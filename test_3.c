#include <numpy.h>
#include <stdio.h>
void main(){
    list x =[1,2,3,4];
     
    int z =sumarr(x);
    printf("%d",z);
    list li1=[3,4,5];
    list li2=[6,9,11];

    list resultli= multiplyarr(li1,li2);
    list y= multiplyarr(resultli,[30,20,10]);

    printarr(resultli);
    printarr(y);

}