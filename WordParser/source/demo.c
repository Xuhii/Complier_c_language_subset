int get(int a, int b, int c){
    a = b + c;
}
int put(int d){
    d += 1;
}
int num1,num2,op,ans,i;
get(num1,num2,op);
for(i=0;i<10;i++;){}

if(op==0)
{
    ans = num1 + num2;
}
if(op==1)
{
    ans = num1 - num2;
}
if(op==2)	    
{
    ans = num1 and num2;
}
if(op==3)
{
    ans = num1 or num2;
}
put(ans);

