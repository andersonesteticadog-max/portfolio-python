vr=float(input('digite o valor do produto:'))
din=float(input('digite o valor recebido em dinheiro:'))
tr=(din-vr)
print('você deve dar o troco no valor de R${:.2f}'.format(tr))
