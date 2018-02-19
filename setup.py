import setuptools
from pip.req import parse_requirements
from pip.download import PipSession


def read_requirements():
    """parses requirements from requirements.txt"""

    install_reqs = parse_requirements('requirements.txt', session=PipSession())
    return [ir.name for ir in install_reqs]


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

        include_package_data=True,

        extras_require={
            'docs': [
                'sphinx==1.2.3',
                'sphinxcontrib-napoleon',
                'sphinx_rtd_theme',
                'numpydoc',
            ],
            'tests': [
                'codecov',
                'pytest',
                'pytest-cov',
                'pytest-pep8',
            ],
        },

        tests_require=[
            'codecov',
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
