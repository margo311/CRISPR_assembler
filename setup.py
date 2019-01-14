from setuptools import setup, find_packages

setup(name='crispr_assembler',
      version='1.0',
      packages=['crispr_assembler',
                'crispr_assembler.utils',
                'crispr_assembler.datastyle',
                'crispr_assembler.main',
                'crispr_assembler.error_correction'],

      package_dir={'':'src'}
      )