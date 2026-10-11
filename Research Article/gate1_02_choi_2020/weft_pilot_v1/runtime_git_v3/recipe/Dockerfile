FROM python@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1
LABEL org.opencontainers.image.version="ravel-numeric-git-v3-20261011"
LABEL org.opencontainers.image.revision="47a2fe5bd07742ddddbd0c5aa5f3e0a4b21172e6"
COPY debs/ /debs/
COPY packages.lock.json /packages.lock.json
COPY verify_os.py /verify_os.py
RUN cd /debs && sha256sum -c SHA256SUMS && dpkg --install /debs/*.deb && apt-get check && python /verify_os.py && test -z "$(dpkg --audit)" && rm -rf /debs
COPY wheels/ /wheels/
COPY requirements.lock /requirements.lock
RUN python -m pip install --no-index --find-links=/wheels --only-binary=:all: --require-hashes -r /requirements.lock && python -m pip check && rm -rf /wheels
ENV MPLBACKEND=Agg OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_NUM_THREADS=4 NUMBA_CACHE_DIR=/tmp/numba MPLCONFIGDIR=/tmp/matplotlib HOME=/tmp
COPY --chmod=0444 synthetic.py /synthetic.py
USER 65534:65534
CMD ["python","-I","/synthetic.py"]
