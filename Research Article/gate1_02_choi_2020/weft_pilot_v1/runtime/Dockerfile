FROM python@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1
COPY wheels/ /wheels/
COPY requirements.lock /requirements.lock
RUN python -m pip install --no-index --find-links=/wheels --only-binary=:all: --require-hashes -r /requirements.lock && python -m pip check && rm -rf /wheels
ENV MPLBACKEND=Agg OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_NUM_THREADS=4 NUMBA_CACHE_DIR=/tmp/numba MPLCONFIGDIR=/tmp/matplotlib HOME=/tmp
COPY --chmod=0444 synthetic.py /synthetic.py
USER 65534:65534
CMD ["python","-I","/synthetic.py"]
