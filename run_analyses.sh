#!/bin/bash
set -e

# Run analyses
python3 /home/scripts/prep_dataframes.py

python3 /home/scripts/covar_correction.py

python3 /home/scripts/HC_normalization.py

python3 /home/scripts/graph_analysis.py

python3 /home/scripts/group_stats.py

python3 /home/scripts/correlations.py

python3 /home/scripts/linear_regressions.py

chmod -R --silent 777 /home/output
chmod -R --silent 777 /home/data

tar -czvf output/output.tar.gz output
