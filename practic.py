folder "prjs" "ior2025torg"
include "ior2025"

'While 1 = 1
  'PDline(80)
'EndWhile
'stop(2, 100)
'line_perekrestok(50,6, 5,2)
'turn_compass(2, 1)

calibreatGrab()
binary(n1, n2)

if n1 < 5 Then
  n1 = 0
Else
  n1 -= 5
EndIf

if n2 < 5 Then
  n2 = 0
Else
  n2 -= 5
EndIf
line_perekrestok(40,4,5,2)
navigator(n2, n1)
grab(gr)
navigator(3, 1)
For i = 1 To 2
  line_perekrestok(40,4,5,2)
line_encoder(50, 20)
EndFor

