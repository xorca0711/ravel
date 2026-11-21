"""Synthetic parser regressions; no biological data or effects."""
import io
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from qualify_sources_v2 import parse_features, parse_reference


class SourceMetadataTests(unittest.TestCase):
    def test_headers_and_values_trimmed_without_rewriting_label(self):
        source = ' id , name , feature_type , multiplexed_sample \n CMO301 , CMO301 , Antibody Capture ," label, 3dpi "\n'
        original, normalized, rows = parse_reference(io.StringIO(source))
        self.assertEqual(original[-1], " multiplexed_sample ")
        self.assertEqual(normalized[-1], "multiplexed_sample")
        self.assertEqual(rows[0], {"id": "CMO301", "name": "CMO301", "feature_type": "Antibody Capture", "multiplexed_sample": "label, 3dpi"})

    def test_missing_header_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing required CSV header"):
            parse_reference(io.StringIO("id,name,feature_type\nCMO301,CMO301,Antibody Capture\n"))

    def test_missing_extra_and_blank_values_rejected(self):
        header = "id,name,feature_type,multiplexed_sample\n"
        for row in ["CMO301,CMO301,Antibody Capture", "CMO301,CMO301,Antibody Capture, ",
                    "CMO301,CMO301,Antibody Capture,label,extra"]:
            with self.subTest(row=row), self.assertRaises(ValueError):
                parse_reference(io.StringIO(header + row + "\n"))

    def test_normalized_header_collision_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate normalized"):
            parse_reference(io.StringIO("id, id ,name,feature_type,multiplexed_sample\n"))

    def test_empty_reference_rejected(self):
        for text in ["", "id,name,feature_type,multiplexed_sample\n"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_reference(io.StringIO(text))

    def test_duplicate_tag_rejected(self):
        header = "id,name,feature_type,multiplexed_sample\n"
        row = "CMO301,CMO301,Antibody Capture,label\n"
        with self.assertRaisesRegex(ValueError, "Duplicate reference tag"):
            parse_reference(io.StringIO(header + row + row))

    def test_blank_csv_lines_skipped(self):
        _, _, rows = parse_reference(io.StringIO("id,name,feature_type,multiplexed_sample\n\nCMO301,CMO301,Antibody Capture,label\n\n"))
        self.assertEqual(len(rows), 1)

    def test_feature_inventory_trims_fields(self):
        counts, tags = parse_features(io.StringIO("gene1\tgene1\tGene Expression\n CMO301 \t CMO301 \t Antibody Capture \n"))
        self.assertEqual(counts, {"Antibody Capture": 1, "Gene Expression": 1})
        self.assertEqual(tags, [{"tag_id": "CMO301", "name": "CMO301", "feature_type": "Antibody Capture"}])

    def test_missing_feature_fields_rejected(self):
        for text in ["", "CMO301\tCMO301\n", "CMO301\t \tAntibody Capture\n"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_features(io.StringIO(text))


if __name__ == "__main__":
    unittest.main()
