# script to make .zip more compact
set -e

find build/lib -name "*-info" -type d -exec rm -rdf {} +
find build/lib -name "tests" -type d -exec rm -rdf {} +
rm -rdf build/lib/boto3/
rm -rdf build/lib/botocore/
rm -rdf build/lib/docutils/
rm -rdf build/lib/dateutil/
rm -rdf build/lib/jmespath/
rm -rdf build/lib/s3transfer/
find build/lib -type f -name '*.pyc' | while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-37//'); cp $f $n; done;
find build/lib -type d -a -name '__pycache__' -print0 | xargs -0 rm -rf
find build/lib -type f -a -name '*.py' -print0 | xargs -0 rm -f