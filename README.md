# Impact of augmentation on basecall accuracy.

Reasearching an impact of specific augemantation of data from Oxford Nanopore Technologies (ONT) sequencers on [RODAN](https://github.com/biodlab/RODAN) - RNA basecaller - accuracy.

## Usage
All detailed results, methods and materials are provided in notebooks and soon will be in seperate report. Here commands are displayed for fitting model with augment data, basecaller and accuracy.

```bash
# Training the model with data augmented via SpecAugment Time Masking
python src/model_with_aug_spec.py -c reduce-rna.config -D OUT_PATH_MODELS -n PROCESS_NAME -l

# basecalling, best model was picked from the training output path based on validation loss
python src/basecall.py TEST_FAST5_DIR -m OUT_PATH_MODELS/*.torch > results/outputs_fasta/FASTA_FILE_NAME.fasta

# aligning output fasta file from basecaller with reference genome, here from gencode.v36 human consortium 
minimap2 -x map-ont --cs -a --secondary=no gencode.v36.transcripts.fa results/outputs_fasta/ASTA_FILE_NAME.fasta > results/FILE_NAME.sam

# evaluating/accuracy
python src/accuracy.py results/FILE_NAME.sam gencode.v36.transcripts.fa
```
This is full pipeline. Validation and training losse will be stored in results/csv_metrics directory. After evaluting basecaller, accuracy will display in CLI. For training and validation dataset please contact me or just add message to Issues tab.
