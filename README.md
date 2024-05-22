# Algoritmo de resolución de sudoku

Un enfoque diferente que también utiliza el retroceso, se basa en el hecho de que en la solución a un sudoku estándar la distribución para cada símbolo individual (valor) debe ser uno de solo 46656 patrones. En el sudoku manual, la resolución de esta técnica se conoce como superposición de patrones o uso de plantillas y se limita a completar solo los últimos valores. Una biblioteca con todos los patrones posibles puede cargarse o crearse al inicio del programa. Luego, a cada símbolo dado se le asigna un conjunto filtrado con esos patrones, que están de acuerdo con las pistas dadas. En el último paso, la parte de retroceso real, los patrones de estos conjuntos se intentan combinar o superponer de una manera no conflictiva hasta que se golpea la única combinación permisible. 

La Implementación es excepcionalmente fácil cuando se usan vectores de bits,porque para todas las pruebas solo se necesitan operaciones lógicas en cuanto a bits, en lugar de cualquier iteración anidada en filas y columnas. Se puede lograr una optimización significativa reduciendo aún más los conjuntos de patrones durante el filtrado. Al probar cada patrón cuestionable contra todos los conjuntos reducidos que ya se aceptaron para los otros símbolos, el número total de patrones que quedan para el retroceso disminuye considerablemente.

# Simple Elimination
Simple Elimination is a fundamental technique that quickly reduces possibilities in cells, especially in the early stages of solving. It's efficient and can drastically simplify the puzzle.

# CSP (Constraint Satisfaction Problem)
CSP covers a wide range of techniques including hidden and naked pairs, triples, and quads. It's a powerful method that systematically eliminates impossible values and finds the remaining viable ones by checking permutations. This method can solve more complex puzzles that simple elimination alone cannot handle.
