import setuptools


def read_requirements():
    """parses requirements from requirements.txt"""

    with open('requirements.txt') as f:
        req = f.readlines()

    return req


if __name__ == "__main__":
    setuptools.setup(
        name='bse_website',
        version="0.1.0",
        description='Website for the Quantum Chemistry Basis Set Exchange',
        author='The Molecular Sciences Software Institute',
        author_email='daltarawy@vt.edu',
        url="https://github.com/MolSSI-BSE/BSE_website",
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
