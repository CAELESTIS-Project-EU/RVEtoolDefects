
def writeJobMN5(file, jobName, totalCPUTimeInHours, queueName, CPUS, account):
    """ Runner queueMN5.sh file
    """
    
    stream = open(file, 'w')

    stream.write('#!/bin/bash\n')
    stream.write('#\n')
    stream.write('#  Submit jobs in MN5\n')
    stream.write('#     sbatch < job.sh\n')
    stream.write('#\n')
    stream.write(f'#SBATCH --job-name={jobName}\n')
    stream.write('#SBATCH --chdir=.\n')
    stream.write('#SBATCH --error=%j.err\n')
    stream.write('#SBATCH --output=%j.out\n')
    stream.write(f'#SBATCH --account={account}\n')
    stream.write(f'#SBATCH --qos={queueName}\n')
    stream.write(f'#SBATCH --ntasks={CPUS}\n')
    stream.write('#SBATCH --cpus-per-task=1\n')
    stream.write('#SBATCH --ntasks-per-node=112\n')
    stream.write('##SBATCH --constraint=highmem\n')
    stream.write(f'#SBATCH --time={totalCPUTimeInHours}:00:00\n')
    stream.write('#\n')
    stream.write('# Load modules for the executable\n')
    stream.write('#\n')
    stream.write('module purge\n')
    stream.write('module load gcc/13.2.0 openmpi/4.1.5-gcc\n')
    stream.write('#\n')
    stream.write('ALYAPATH="/gpfs/projects/bsce81/alya/builds/Alya_mn5gcc.x"\n')
    stream.write(f'PROBLEMNAME={jobName}\n')
    stream.write('#\n')
    stream.write('# Launches ALYA\n')
    stream.write('#\n')
    stream.write('srun $ALYAPATH $PROBLEMNAME\n')
    
    stream.close()

    return

def writeJobNO3(file, jobName, totalCPUTimeInHours, queueName, CPUS, account):
    """ Runner queueNO3.sh file
    """
    
    stream = open(file, 'w')

    stream.write('#!/bin/bash\n')
    stream.write('#\n')
    stream.write('#  Submit jobs in NO3\n')
    stream.write('#     sbatch < job.sh\n')
    stream.write('#\n')
    stream.write(f'#SBATCH --job-name={jobName}\n')
    stream.write('#SBATCH --chdir=.\n')
    stream.write('#SBATCH --error=%j.err\n')
    stream.write('#SBATCH --output=%j.out\n')
    stream.write(f'#SBATCH --account={account}\n')
    stream.write(f'#SBATCH --qos={queueName}\n')
    stream.write(f'#SBATCH --ntasks={CPUS}\n')
    stream.write('#SBATCH --cpus-per-task=1\n')
    stream.write('#SBATCH --ntasks-per-node=16\n')
    stream.write('##SBATCH --constraint=highmem\n')
    stream.write(f'#SBATCH --time={totalCPUTimeInHours}:00:00\n')
    stream.write('#\n')
    stream.write('# Load modules for the executable\n')
    stream.write('#\n')
    stream.write('module purge\n')
    stream.write('module load intel/2021.4 impi/2021.4\n')
    stream.write('#\n')
    stream.write('ALYAPATH="/gpfs/projects/bsce81/alya/builds/Alya_no3.x"\n')
    stream.write(f'PROBLEMNAME={jobName}\n')
    stream.write('#\n')
    stream.write('# Launches ALYA\n')
    stream.write('#\n')
    stream.write('srun $ALYAPATH $PROBLEMNAME\n')
    
    stream.close()

    return
