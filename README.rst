=====================
SIERRA Sample Project
=====================

This is a collection of SIERRA project plugins to illustrate how to use SIERRA
with:

- ARGoS

- ROS1+Gazebo

- ROS1+Robot (experiment generation only)

- JSONSIM (Stub engine taking in .json files)

- YAMLSIM (Stub engine taking in .yaml files)

Between all project plugins, examples of the following are cumulatively
provided:

- Using stage5 to compare deliverables

- Creating a new batch criteria

- Bivariate batch criteria capability

To use this repo to try out/get started with SIERRA, see `Trying Out SIERRA
<https://sierra.readthedocs.io/en/master/src/trial.html>`_ and `Getting Started
With SIERRA <https://sierra.readthedocs.io/en/master/src/startup.html>`_,
respectively.

Repo Structure
==============

This repo is organized as follows:

├── argos/
│   ├── CMakeLists.txt
│   ├── include
│   └── src
├── exp/
│   ├── argos/
│   ├── jsonsim/
│   ├── ros1gazebo/
│   ├── ros1robot/
│   └── yamlsim/
├── LICENSE.md
├── plugins/
│   ├── __init__.py
│   ├── jsonsim/
│   ├── __pycache__
│   └── yamlsim/
├── projects/
│   ├── sample_argos/
│   ├── sample_jsonsim/
│   ├── sample_ros1gazebo/
│   ├── sample_ros1robot/
│   └── sample_yamlsim/
└── README.rst

At the top level:

- ``argos/`` - Has some simple foraging code stolen from `here
  <https://github.com/ilpincy/argos3-examples>`_ to provide a non-trivial agent
  controller for the purposes of demonstration.

- ``exp/`` - Has experimental input templates to be passed to SIERRA via
  ``--expdef-template`` for all the example projects. Organized by engine.

- ``plugins/`` - Engine plugins for some sample projects, demonstrating that new
  engine plugins can be defined outside of SIERRA and consumed.

- ``projects/`` - The project plugin code for each sample project, organized by
  engine (1:1 mapping).
