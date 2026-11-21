//! Single-pass native fragment coverage. Coordinates and raw export IDs are preserved.
use std::collections::{HashMap, HashSet};
use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};

#[derive(Default)]
struct Depth { unique: u64, autosomal: u64, mitochondrial: u64, support: u64, repeats: u64 }

fn number(field: &[u8]) -> u64 {
    assert!(!field.is_empty());
    field.iter().fold(0, |n, &b| { assert!(b.is_ascii_digit()); n * 10 + (b-b'0') as u64 })
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    assert_eq!(args.len(),4);
    let mut targets: HashMap<Vec<u8>,Vec<(u64,u64)>> = HashMap::new();
    for line in BufReader::new(File::open(&args[1])?).lines() {
        let row=line?;
        let cols: Vec<&[u8]> = row.as_bytes().split(|&b| b==b'\t').collect();
        targets.entry(cols[0].to_vec()).or_default().push((number(cols[1]),number(cols[2])));
    }
    for windows in targets.values_mut() { windows.sort(); }
    let mut raw_targets=BufWriter::new(File::create(&args[3])?);
    writeln!(raw_targets,"chrom\tstart\tend\tbarcode\tread_support")?;
    let mut id_by_barcode=HashMap::<Vec<u8>,usize>::new();
    let mut depths:Vec<Depth>=Vec::new();
    let mut seen_chrom=HashSet::<Vec<u8>>::new();
    let mut at_start=HashSet::<(usize,u64)>::new();
    let mut chrom=Vec::<u8>::new();
    let mut previous_start=0;
    let mut autosomal=false;
    let mut mito=false;
    let mut windows:&[(u64,u64)]=&[];
    let mut first_window=0;
    let stdin=io::stdin();
    let mut input=BufReader::with_capacity(1024*1024,stdin.lock());
    let mut line=Vec::with_capacity(256);
    loop {
        line.clear();
        if input.read_until(b'\n',&mut line)?==0 {break;}
        let record=line.strip_suffix(b"\n").unwrap_or(&line);
        let record=record.strip_suffix(b"\r").unwrap_or(record);
        let mut fields=record.split(|&b| b==b'\t');
        let ctg=fields.next().unwrap();
        let start=number(fields.next().unwrap());
        let end=number(fields.next().unwrap());
        let barcode=fields.next().unwrap();
        let support=number(fields.next().unwrap());
        assert!(fields.next().is_none() && start<end && support>0 && !barcode.is_empty());
        if ctg!=chrom {
            assert!(seen_chrom.insert(ctg.to_vec()),"noncontiguous chromosome");
            chrom=ctg.to_vec(); previous_start=0; at_start.clear(); first_window=0;
            windows=targets.get(ctg).map(Vec::as_slice).unwrap_or(&[]);
            let suffix=ctg.strip_prefix(b"chr").unwrap_or(b"");
            autosomal=!suffix.is_empty() && suffix.iter().all(u8::is_ascii_digit) && (1..=19).contains(&number(suffix));
            mito=ctg==b"chrM";
        }
        assert!(start>=previous_start,"fragment starts not sorted within chromosome");
        if start!=previous_start { at_start.clear(); previous_start=start; }
        let id=if let Some(v)=id_by_barcode.get(barcode) { *v } else {
            let i=depths.len(); depths.push(Depth::default()); id_by_barcode.insert(barcode.to_vec(),i); i
        };
        let d=&mut depths[id];
        d.support+=support;
        if !at_start.insert((id,end)) { d.repeats+=1; continue; }
        d.unique+=1; if autosomal {d.autosomal+=1;} if mito {d.mitochondrial+=1;}
        while first_window<windows.len() && windows[first_window].1<=start {first_window+=1;}
        if first_window<windows.len() && windows[first_window].0<end {
            raw_targets.write_all(record)?; raw_targets.write_all(b"\n")?;
        }
    }
    raw_targets.flush()?;
    let mut depth=BufWriter::new(File::create(&args[2])?);
    writeln!(depth,"barcode\tunique_fragments\tautosomal_unique\tmitochondrial_unique\tread_support\tduplicate_rows")?;
    let mut keys:Vec<_>=id_by_barcode.into_iter().collect();
    keys.sort_unstable_by(|a,b| a.0.cmp(&b.0));
    for (key,id) in keys {
        depth.write_all(&key)?;
        let d=&depths[id]; writeln!(depth,"\t{}\t{}\t{}\t{}\t{}",d.unique,d.autosomal,d.mitochondrial,d.support,d.repeats)?;
    }
    depth.flush()
}
