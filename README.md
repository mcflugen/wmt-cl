# wmt-cl
Command-line tools for the Web Modeling Tool

## Saving and Running a Model

    id=$(wmt model save model.yaml)
    wmt simulation save $id Testing
    wmt simulation launch

