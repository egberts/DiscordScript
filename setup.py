# encoding=utf-8
from setuptools import setup

setup(name="DiscordScript",
      version="0.2.0",
      description="Simple scripting Language for Discord Bots. VERY Beta",
      author="Jacob Jäger",
      author_email="jcb1317@protonmail.com",
      url="https://github.com/jcb1317/discordscript",
      packages=["discordscript"],
      entry_points={
          'console_scripts': [
              "discordscript=discordscript.cli:main"
          ]
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Embedded Systems',
          'Topic :: Software Development :: Interpreters'
      ],
      keywords="language discord scripting script tatsu parser interpreter",
      install_requires=["tatsu", "discord.py"],
      )
