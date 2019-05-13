from setuptools import setup, find_packages

setup(name='crispr_assembler',
      version='1.0',
      packages=['crispr_assembler',
                'crispr_assembler.utils',
                'crispr_assembler.datastyle',
                'crispr_assembler.main',
                'crispr_assembler.error_correction',
                'crispr_assembler.assemblers',
                'crispr_assembler.splitter',
                'crispr_assembler.fastq_processor',
                'crispr_assembler.alignments',
                'crispr_assembler.assemblers',
                'crispr_assembler.comparator',
                ],

      package_dir={'':'src'}
      )