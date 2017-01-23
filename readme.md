How it works
============

We define `input.txt` and `desop.txt`, which are input and desired output files for the code that 
the applicant will write.

The Program Evaluator will feed `input.txt` to the program submitted by the applicant and 
generated an `actop.txt` (Actual Output).

There is another subroutine which will comare desop.txt and actop.txt and if it matches, 
then we proceed to compute the time complexity. If it's O(1) (based on the running times for 
inputs at different scale 10, 100, 1000, 1000...), then we accept the solution with a js alert saying
"Accepted" (for now) or else "Rejected" with a proper reason (Wrong Answer, Timeout, etc).

actop.txt will be generated separately for each applicant i.e. randomly for each request (there's a
requestId for each applicant who submits code).