import os
import sys
import glob
import shlex
import subprocess

samples = {}

for count, filename in enumerate(sys.argv[1:]):
    #if count > 1: break
    base_name = os.path.splitext(filename)[0]
    run_name = os.path.split(base_name)[-1]
    output = os.path.split(filename)[0]
    if samples.has_key(run_name.split(".")[0]) == False:
        samples[run_name.split(".")[0]] = [filename]
    else:
        samples[run_name.split(".")[0]] += [filename]

for sample in samples.keys():

    cli = """qsub -V -N {1} -pe omp {0}  -l h_rt=10:00:00 -b y \
    java -Xmx2g -Djava.io.tmpdir=/scratch/\
    -jar /projectnb/mullenl/programs/GenomeAnalysisTK-2.0-39-gd091f72/GenomeAnalysisTK.jar \
    -T RealignerTargetCreator \
    --num_threads {0} """.format('4',sample)

    for s_part in samples[sample]:
        cli += "-I {} ".format(s_part)

    cli += """-R ../bothalleles.fasta \
    -o {2}.intervals \
    """.format(base_name,output,sample)
    #print cli
    cli_parts = shlex.split(cli)
    print "executing: {0}".format(sample)
    ft = subprocess.Popen(cli_parts, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()

