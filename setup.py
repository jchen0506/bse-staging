import setuptools
from pip.req import parse_requirements
from pip.download import PipSession


def read_requirements():
    """parses requirements from requirements.txt"""
    install_reqs = parse_requirements('requirements.txt', session=PipSession())
    reqs = [ir.name for ir in install_reqs]
    print(reqs)
    return reqs


if __name__ == "__main__":
    setuptools.setup(
        name='bse_website',
        version="0.1.0",
        description='Website for the Quantum Chemistry Basis Set Exchange',
        author='The Molecular Sciences Software Institute',
        author_email='daltarawy@vt.edu',
        url="https://github.com/doaa-altarawy/BSE_website",
        license='BSD-3C',
        packages=setuptools.find_packages(),

        install_requires=read_requirements(),

        extras_require={
            'docs': [
                'sphinx==1.2.3',  # autodoc was broken in 1.3.1
                'sphinxcontrib-napoleon',
                'sphinx_rtd_theme',
                'numpydoc',
            ],
            'tests': [
                'pytest',
                'pytest-cov',
                'pytest-pep8',
            ],
        },

        tests_require=[
            'pytest',
            'pytest-cov',
            'pytest-pep8',
        ],

        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
        ],
        zip_safe=True,
    )
