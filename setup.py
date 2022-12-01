from setuptools import setup

setup(
    name='slimevolleygym',
    version='0.1.0',
    keywords='games, environment, agent, rl, ai, gym',
    url='https://github.com/hardmaru/slimevolleygym',
    description='Slime Volleyball Gym Environment',
    packages=['slimevolleygym'],
    install_requires=[
        'gym==0.19.0',
        'numpy>=1.13.0',
        'opencv-python>=3.4.2.0',
        'stable-baselines[mpi]==2.10.0',
        'tensorflow==1.14.0'
    ]
)
