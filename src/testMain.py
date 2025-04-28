from Compiler import Compiler
import analex

test_lines = """Keyword 12      0       9       procedure
Identifier      12      10      2       pp
Keyword 12      13      2       is
Identifier      13      2       1       i
Character       13      3       1       ,
Identifier      13      4       1       j
Character       13      5       1       :
Keyword 13      6       7       integer
Character       13      13      1       ;
Keyword 14      0       5       begin
Identifier      15      2       1       i
Symbol  15      3       2       :=
Integer 15      5       1       1
Character       15      6       1       ;
Keyword 19      2       5       while
Identifier      19      8       1       i
Symbol  19      9       2       /=
Integer 19      11      1       5
Keyword 19      13      4       loop
Identifier      20      4       1       j
Symbol  20      5       2       :=
Integer 20      7       1       1
Character       20      8       1       ;
Keyword 24      4       5       while
Identifier      24      10      1       j
Symbol  24      11      2       /=
Integer 24      13      1       5
Keyword 24      15      4       loop
Keyword 25      6       3       put
Character       25      9       1       (
Identifier      25      10      1       j
Character       25      11      1       )
Character       25      12      1       ;
Identifier      26      6       1       j
Symbol  26      7       2       :=
Identifier      26      9       1       j
Character       26      10      1       +
Integer 26      11      1       1
Keyword 27      4       3       end
Character       27      8       1       ;
Identifier      28      4       1       i
Symbol  28      5       2       :=
Identifier      28      7       1       i
Character       28      8       1       +
Integer 28      9       1       1
Keyword 29      2       3       end
Keyword 30      0       3       end
Fel     30      3       1       ."""

compiler = Compiler(test_lines, "quoicoubeh")
compiler.main()