The Evaluator Math input type is used with Numerical and Formula responses
which have evaluation methods for verification of symbolic problems. It allows
the student to enter in complicated math expressions with (in the case of
FormulaResponse) instructor-defined variables.

XML tag
Either a `<numericalresponse>` or a `<formularesponse>` with a `<formulaequationinput>` sub element.

Example problem.

```
<numericalresponse answer="3.14159">
  <responseparam type="tolerance" default=".02" />
  <formulaequationinput />
</numericalresponse>
```
