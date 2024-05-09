#include <stdio.h>

int testfunc(int param1){
  return param1+5;
}

void main() {

  // int x[];
  
  // str test=openfile("hello.txt");
  // printf("%s",test);
  int x =5, z =7;
  int y =8;
  int i ;
  str b= "hello world" ;
  list arr=[1,2,3,4,'c'];
  printarr(arr);
  
  
  if(testfunc(1)==6){
    printf("true\n");
  }
  else{
    printf("false");
  }
  switch (x){
    case (7) {
      printf("5");
    }
    case (6){
      printf("6");
    }
    default{
      printf("not found");
    }
  }

  // int z = 'c';
  // int x = 5;
  // printf("%s",x);
  // if (x ==0){
  //   printf("x=0");
  // }
  
  // for ( i = 0; i < x; i++){
  //   printf("hello");
  // }
  

}
