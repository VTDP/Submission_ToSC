1. About The Solver
This is the source codes for modeling a linear layer and finding BDP for LED, MISTY1, CLEFIA, CAMELLIA and AES.
It is written with python3. 
When you run the codes here and you will first get the STP input file *.cvc, then you need to run this cvc file in a STP solver.
Therefore, you need to install the STP solver in advance. 
The STP solver is availuable in https://stp.github.io. 
STP solver, as other SMT solver, requires a SAT solver as its foundmental solver, minisat is the default SAT solver for STP.
However, we strongly recommend installing cryptominisat and recall the cryptominisat solver when you run the STP solver.

2. The Structure of the Source Codes and their function. 
The files marked by * are all independent, you do not need to wrong about the depencies among them.
Below the comments "file for modeling BDP for ciphers", there are 7 directories.
We only list the structure of "AES_4_keydependent" but it is similar in other 6 directories.
----------------------------------------------------------
|---- Submission_ToSC
    # file for modeling matrix
    *|---- Matrix_if_then_else.py
    *|---- Matrix.py

    # file for modeling BDP for ciphers
    *|---- AES_4_keydependent
          |---- AES_4_round_keydependent.py
          |---- AES.py
          |---- AssertSbox.py
          |---- constant.py
          |---- Matrix_non_square.py
          |---- Matrix.py
          |---- BOOLFUNC
                |---- GenInt.py
                |---- __init__.py
                |---- Polynomial.py
                |---- README.md
                |---- Sbox.py
                |---- Term.py
                |---- test.py
                |---- Vector.py

    *|---- AES_5_keydependent
    *|---- CAMELLIA
    *|---- CLEFIA
    *|---- LED_6r
    *|---- LED_7r
    *|---- Misty1_6_round_62_active
    *|---- Misty1_6_round_63_active

    # readme
    *|---- README.md
-----------------------------------------------------------------

* Matrix_if_then_else.py and Matrix.py:
    They are two kinds of implementations of our model in paper. 
    Matrix_if_then_else.py follows the principle introduced in Section 4.1.
    While Matrix.py follows Theorem 2.
    Now, for MISTY1 and CAMELLIA, only Matrix_if_then_else.py is allowed, because there are many matriced used in the main function.
    For other cipers, Matrix.py and Matrix_if_then_else.py are all allowed.

* AES_4_keydependent:  
    Codes for verify the 4-round key-dependent distinguisher of AES introduced in Section 5.1.
    AES_4_round_keydependent.py is the main function, use the command to run it:
    ($ is the prompt of bash)
    _____________________________________
    $ python3 AES_4_round_keydependent.py 
    _____________________________________
    the output is the content of our cvc file, use the redirection command to make them in any file with a cvc extent.

    $ python3 AES_4_round_keydependent.py > AES_4.cvc
    When the cvc file gotten, you can run it in your computer,
    _____________________________________
    $ stp AES_4.py 
    _____________________________________

    The default minisat solver is used to solver the fundamental SAT problems.
    If you have installed the cryptominisat, you can also use the command to recall cryptominisat by manual,
    _____________________________________
    $ stp AES_4.py --cryptominisat --threads n
    _____________________________________
    
    Cryptominisat supports paralleling, so you can use --threads n to decide how many threads you need to solver the problem.
    by experiments, we recommend n=4.
    
    After some time running, you may get two kinds of results returned.
    1. Valid. 
    2. Invalid.
    CVC file ended with a statement "QUERY FALSE" is aksing a question to the solver 
    "No solutions to the constriants I list in the cvc file, right?" 
    So "Valid." means the no solution to the model while "Invalid." means there is at least one solution.
    As is well known in division property, no solution is a good news that we find some balanced bits. 

* AES_5_round_keydepent:
    similar with AES_4_round_keydependent
    -------------------------------------------------
    $ python3 AES_5_round_keydependent.py > AES_5.cvc  
    -------------------------------------------------
    $ stp AES_5.cvc (--cryptominisat --threads 4)
    -------------------------------------------------

* CAMELLIA
    In the Camellia_base.py, we list the model of camellia.
    In Camellia.py, you can change the inVec to decide which bits should be active and how many rounds you want to check.  
    -------------------------------------------------
    $ python3 Camellia.py > camellia.cvc
    -------------------------------------------------
    $ stp camellia.cvc (--cryptominisat --threads 4)
    -------------------------------------------------

* CLEFIA
    -------------------------------------------------
    $ python3 CLEFIA.py > CLEIFA.cvc
    -------------------------------------------------
    $ stp CLEFIA.cvc (--cryptominisat --threads 4)
    -------------------------------------------------

* LED_6r
    -------------------------------------------------
    $ python3 led.py > led.cvc
    -------------------------------------------------
    $ stp led.cvc (--cryptominisat --threads 4)
    -------------------------------------------------

* LED_7r
    -------------------------------------------------
    $ python3 led.py > led.cvc
    -------------------------------------------------
    $ stp led.cvc (--cryptominisat --threads 4)
    -------------------------------------------------

* Misty1_6_round_62_active
    -------------------------------------------------
    $ python3 Misty1.py > Misty1_62.cvc
    -------------------------------------------------
    $ stp Misty1_62.py (--cryptominisat --threads 4)
    -------------------------------------------------

* Misty1_6_round_63_active
    -------------------------------------------------
    $ python3 Misty1.py > Misty1_63.cvc
    -------------------------------------------------
    $ stp Misty1_63.py (--cryptominisat --threads 4)
    -------------------------------------------------

