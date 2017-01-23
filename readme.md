**Program Evaluator**
==================

Source Code Evaluation Service, to accept or reject a solution on the http://activesphere.com/careers page.

Installation
--------------
1. Install `python` and `pip`
2. Setup a new virtual environment for this project by running the command **from within the project
   dir**: `virtualenv .` 
3. Activate the virtual environment **from within the project dir**: `. bin/activate`
3. Install all requirements: `pip install -r requirements.txt`
4. You can start the server with the command: `./start_server`


Adding New Problems and their input/desop files
-----------------------------------------------

New problems can be added to the `src/problems/` dir. Steps to create a new problems are as
follows:

1. Create a new folder under `src/problems/`.
2. Add the `input_scale.txt` and `desop_scale.txt` files where *scale* can vary as per
   requirements.
3. Register the new problem with the service by adding it to the `PROB_MAPPING` in `src/config.py`.
4. Restart the service for it to take effect.

How it works
-------------

We define `input.txt` and `desop.txt`, which are input and desired output files for the code that
the applicant will write.

The Program Evaluator will feed `input.txt` to the program submitted by the applicant and generated
an `actop.txt` (Actual Output).

There is another subroutine which will comare `desop.txt` and `actop.txt` and if it matches, then we
proceed to compute the time complexity. If it's `O(1)` (based on the running times for inputs at
different scale 10, 100, 1000, 1000...), then we accept the solution with a js alert saying
**Accepted** (for now) or else **Rejected** with a proper reason (Wrong Answer, Timeout, etc.).

`actop.txt` will be generated separately for each applicant i.e. randomly for each request (there's
a `requestId` for each applicant who submits code).

