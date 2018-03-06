.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==============
Project Stage Validators
==============

This module adds a control restriction to the stages from tasks and issues. If a stage is marked as "Needs validation", only the users selected as "Validators" on the project will be able to move the tasks and issues to that stage.

Installation
============

To install this module, you need to:

#. No special installation is required.

Configuration
=============

To configure this module, you need to:

#. Go to Project > Configuration > Stages to mark the stage on which you need a validation before.

.. figure:: project_stage_validator/static/src/img/configuration1.jpeg
   :alt: Configuration 1
   :width: 600 px

#. Go to Project > Select the project > More > Settings.
You'll find a page called Validators in which you specify which users can move the tasks and issues to the stage marked as "Needs validation".

.. figure:: project_stage_validator/static/src/img/configuration2.jpeg
   :alt: Configuration 2
   :width: 600 px

Usage
=====

To use this module, you need to:

#. Go to ...

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/140/10.0

.. repo_id is available in https://github.com/OCA/maintainer-tools/blob/master/tools/repos_with_ids.txt
.. branch is "8.0" for example

Known issues / Roadmap
======================

* ...

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/project/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://odoo-community.org/logo.png>`_.

Contributors
------------

* Xavier Jiménez <xavier.jimenez@qubiq.es> (www.qubiq.es)

Do not contact contributors directly about support or help with technical issues.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
