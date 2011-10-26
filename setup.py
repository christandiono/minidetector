from distutils.core import setup
 
setup(
    name='minidetector',
    version='1.1',
    description='Django middleware and view decorator to detect phones and small-screen devices',
    long_description = open("readme.markdown").read(),
    author='metamoof, Chris Drackett',
    url = "http://code.google.com/p/minidetector/",
    packages = [
        "minidetector",
        "minidetector.tests",
    ],
    package_data={
        "minidetector": ["search_strings.txt"]
    },
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
