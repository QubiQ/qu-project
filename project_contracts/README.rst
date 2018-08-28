.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================
Project Contracts
=================

This module brings back the contracts management but without the recurring invoicing features.
Since in previous versions a project could have issues and tasks, a single project / contract was made, but now they can not go together in the same project, therefore a contract can have more than one project at a time.

Installation
============

Just install


Configuration
=============

In the category of products that contain the products used for the sale of contract hours, you must check the option 'Contract hours'.


Usage
=====

#.In Project/Contracts/Contracts, can create one new contract. In a task if it is related to a project and this to a contract only an imputation can be added if the contract is open.
#.There is a cron that checks contracts daily to verify that if they are in negative hours and their status is open, they change to renew and send an email to the contract manager informing them.
#.To increase the maximum hours of a contract, you must make a sale / invoice to the customer of the contract with a product of the category where the check 'Contract hours' has been placed.


Gestión de errores
==================

Los errores/fallos se gestionan en `las incidencias de GitHub <https://github.com/QubiQ/qu-project/issues>`_.
En caso de problemas, compruebe por favor si su incidencia ha sido ya
reportada. Si fue el primero en descubrirla, ayúdenos a solucionarla indicando
una detallada descripción `aquí <https://github.com/QubiQ/qu-project/issues/new>`_.


Credits
=======

Authors
~~~~~~~

* Valentin Vinagre <valentin.vinagre@qubiq.es>


Maintainer
~~~~~~~~~~

This module is maintained by QubiQ.
