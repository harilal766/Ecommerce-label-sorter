On the input file of scheduled orders, a single amazon order will have
pages explained below

### Shipping Label
Contains the qr and bar codes , and other shipping  details regarding the order.
### Invoice
Contains the order details, example can be found in this link : https://www.scribd.com/document/443274541/Amazon-Invoice-pdf
### Additional invoice page
 packing label,invoice and sometimes an additional page of the invoice as documents in the scheduled orders file.

The additional page mentioned above occurs rarely in a scheduled file, this program will remove it if occurs,


The product datas are stored in a table in the invoice page. 
this table is analyzed to get the product name and quantities
and added to a summary dict.





