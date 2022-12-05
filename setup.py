from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  "Programming Language :: Python :: 3",
  "Operating System :: Unix",
  "Operating System :: MacOS :: MacOS X",
  "Operating System :: Microsoft :: Windows",
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='fasteda',
  version='1.0.0',
  description='A module to get a quick overview of a DataFrame',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Matt OP',
  license='MIT', 
  classifiers=classifiers,
  keywords=['python', 'data', 'dataframe', 'data analysis', 'eda', 'pandas', 'numpy'], 
  packages=find_packages(),
  install_requires=['pandas', 'numpy', 'matplotlib', 'seaborn', 'missingno', 'colorama'] 
)
