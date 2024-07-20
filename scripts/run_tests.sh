rm -rf reports

python -m pytest \
  --numprocesses=auto \
  --cov=walkingpadfitbit \
  --cov-report=xml \
  --cov-report=html \
  --junitxml="reports/junit.xml" \
  --log-cli-level=DEBUG \
  --log-cli-format="[%(asctime)s][%(levelname)-7s][%(name)-10s] %(message)s" \
  tests

mkdir -p reports
mv coverage.xml htmlcov reports/.
