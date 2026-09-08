default: check

# Structural checks only; live agent evaluation is a separate activity.
check:
    python3 -m unittest discover -s tests -v
    git diff --check
