---
title: 程序设计(A)(C)作业
date: 2025-10-09
author: Tzxy
categories:
- [程序设计(A)(C)]
tags:
  - 作业
  - 程序设计
  - C语言
---

# 程序设计(A)(C)作业

写在前面
第一次作业写的很烂，第二次作业开始将使用代码块，以增强可读性。
第四次作业开始将把每道题提供一个省流写在标题处。

# 实验作业01-熟悉实验环境并理解数据类型
## T2
> 题目：编写程序，求方程$ax^2+bx+c=0$的根，用户输入a,b,c的值，程序输出显示方程的解。

==解：==
结果如图：
![图片](</images/程序设计(A)(C)/7ab1c4b360ae9c78ac7d92401c7eb3f6.png>)

## T3
> 题目：实现个人信息的输出，包括学号、姓名、高中学校、手机号、座右铭。

==解：==
结果略

## T4
> 题目：输入下图代码，运行结果是什么？并解释说明 sizeof的功能和用法。![图片](</images/程序设计(A)(C)/Pasted_image_20251009180237.png>)

==解：==
结果如图：
![图片](</images/程序设计(A)(C)/049289e9ea31718ae5ac20e5ebdb87b8.png>)
**修改代码后得到结果：**
![图片](</images/程序设计(A)(C)/a6e7a376a35c0b6688b5a005fa6b7903.png>)
sizeof的功能和用法：
1. 获取目标在内存中所占的字节数；
2. 用法为sizeof()

## T5
> 题目：理解： C语言中字符型数据和整型数据之间可以通用，补充完整如下代码，运行结果是什么，为什么？

```
c1,c2;
c1=’A’;
c2=c1+300;
printf(“c1=%c,c2=%c\n”,c1,c2);
printf(“c1=%d,c2=%d\n”,c1,c2);
```

==解：==
结果如下：
![图片](</images/程序设计(A)(C)/82495cc01dfa7320d88bfc5ae7ff330f.png>)
原因：
1. 第一行是输出字符型数据，故输出A和m【（65+300）%256=109对应m】；
2. 第二行输出整型数据，故输出65和109

# 实验作业02-数据类型与运算
## T1
题目：
> 编写程序，显示：
> 1. char/int/short/long/long long/float/ double/long double等数据类型所占内存空间的大小；
> 2. 22%4 ,  -22%4,  22%（-4）,  -22%（-4）四个表达式的输出结果.

==解：==
（1）
```
#include <stdio.h>

int main()
{
    printf("char的大小为%zu字节\n",sizeof(char));
    printf("int 的大小为%zu字节\n", sizeof(int));
    printf("short 的大小为%zu字节\n", sizeof(short));
    printf("long 的大小为%zu字节\n", sizeof(long));
    printf("long long 的大小为%zu字节\n", sizeof(long long));
    printf("float 的大小为%zu字节\n", sizeof(float));
    printf("double 的大小为%zu字节\n", sizeof(double));
    printf("long double 的大小为%zu字节\n", sizeof(long double));

    return 0;
}
```
输出结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251016212658.png>)
（2）
```
#include <stdio.h>

int main()
{
    printf("22%4的输出结果为%d\n",22%4);
    printf("-22%4的输出结果为%d\n",(-22)%4);
    printf("22%(-4)的输出结果为%d\n",22%(-4));
    printf("(-22)%(-4)的输出结果为%d\n",(-22)%(-4));
  
    return 0;
}
```
输出结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251016213338.png>)

## T2
题目：
> 编写程序，分别使用符号常量和const常量定义π，从键盘输入圆的半径r（r为float类型），计算并输出圆的周长和面积。

==解：==
1. 用符号常量
```
#include <stdio.h>
#define PI 3.14159265358979323

int main()
{
    float r=0,c=0,S=0;
    printf("请输入圆的半径：");
    scanf("%f",&r);
    c=2*PI*r;
    S=PI*r*r;
    printf("圆的周长为%f",c);
    printf("圆的面积为%f",S);

    return 0;
}
```
输出结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251016214944.png>)
2. 用const常量
```
#include <stdio.h>

int main()
{
    float r=0,c=0,S=0;
    const float PI=3.1415926;
    printf("请输入圆的半径：");
    scanf("%f",&r);
    c=2*PI*r;
    S=PI*r*r;
    printf("圆的周长为%f",c);
    printf("圆的面积为%f",S);
    
    return 0;

}
```
输出结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251016215232.png>)

## T3
题目：
> 编写程序，输入一个整数，判断其奇偶性，并输出显示。

==解：==
```
#include <stdio.h>

int main()
{
    int a=0;
    printf("请输入一个整数：");
    scanf("%d",&a);
    if(a%2==0)printf("这是一个偶数\n");
    else printf("这是一个奇数\n");

    return 0;
}
```
输出结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251016220726.png>)

## T4
题目：
> 编写程序，实现华氏温度到摄氏温度的转换。

==解：==
（本人在之前已经做过一个摄氏度华氏度的转换的程序了，在此提供一个优化版本。）
```
#include <stdio.h>

int main()
{
    printf("请选择转换机制\n【A】摄氏度转华氏度\n【B】华氏度转摄氏度\n");
    float a=0,b=0;
    char choice;
    scanf("%c",&choice);
    if(choice=='A')
    {
        scanf("%f",&a);
        printf("%f华氏度\n",b=a*9/5+32);
    }
    else if(choice=='B')
    {
        scanf("%f",&a);
        printf("%f摄氏度\n",b=(a-32)*5/9);
    }
    else
    {
        printf("输入错误\n");
    }

    return 0;
}
```
输出结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251016221253.png>)

## T5
题目：
> 编写程序，从键盘输入三角形的三个边长a，b，c的值，计算并输出三角形的面积。当3条边无法构成三角形时，输出“无法构建三角形！”

==解：==
```
#include <stdio.h>
#include <math.h>

int main()
{
    double a=0,b=0,c=0;
    printf("请输入三角形三边长：");
    scanf("%lf%lf%lf",&a,&b,&c);
    if(a+b>c && b+c>a && c+a>b)
    {
        double p=(a+b+c)/2;
        printf("%lf",sqrt(p*(p-a)*(p-b)*(p-c)));
    }
    else
    {
        printf("无法构建三角形！");
    }

    return 0;
}
```
输出的结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251017002425.png>)

## T6
题目：
> 编写程序，从键盘任意输入一个3位整数，输出它的逆序数（忽略整数前的正负号）。例如，输入123，输出321。

==解：==
```
#include <stdio.h>

int main()
{
    printf("请输入一个三位正整数：");
    int a=0,b=0,s=0,g=0;
    scanf("%d",&a);
    b=(a/100)%10;
    s=(a/10)%10;
    g=a%10;
    printf("%d%d%d\n",g,s,b);

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251017004011.png>)

## T7
题目：
> 编写程序，将China译成密码，密码规律是：用原来的字母后面第4个字母代替原来的字母。例如，字母A后面的第4个字母是E，用E代替A。因此China应该译为Glmre。

==解：==
> 此题有借助ChatGPT来学习、完成。
```
#include <stdio.h>

int main()
{
    char word[20];
    printf("请输入一个单词：");
    scanf("%s",word);
    int i=0;
    while(word[i]!='\0')    //'\0'表示字符串结束
    {
        char a=word[i];
        if(a>='A' && a<='Z')
        {word[i]=(a-'A'+4)%26+'A';}
        else if(a>='a' && a<='z')
        {word[i]=(a-'a'+4)%26+'a';}
        i++;
    }
    printf("凯撒密码加密后结果为：%s\n",word);

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251017012213.png>)
## T8（选做题）
题目：
> 编写一个幼儿知识小测验程序，给出3道知识题，由幼儿回答，幼儿回答后可以自己将答案与系统答案比较，并记录是否正确，最后输出测验成绩。请补充12，19，26行代码，并回答第7行注释中的问题。
> ![图片](</images/程序设计(A)(C)/Pasted_image_20251017012309.png>)

==解：==
补全代码如下：
```C
#include <stdio.h>

int main(void){
    char answer,YesorNot;
    printf("***---幼儿知识小测验程序---***\n");
    printf("\n1、熊猫是熊吗？是，键入Y;否，键入N：");
    answer=getchar();getchar(); //清除多余回车
    printf("熊猫不是熊，此题答案是：N\n");
    printf("你的答案对吗？正确键入1；错误键入0：");
    YesorNot=getchar();getchar();
    int score=0;//赋值语句计算分数，补充在第12行
    if(YesorNot=='1') score++;
    printf("\n2、小海马是由爸爸生的，对吗？是，键入Y；否，键入N：");
    answer=getchar();getchar();
    printf("海马是由雄海马生的，此题答案是Y\n");
    printf("你的答案对吗？正确键入1；错误键入0：");
    YesorNot=getchar();getchar();
    //赋值语句计算分数，补充在第19行
    if(YesorNot=='1') score++;
    printf("\n3. 世界上最大的鱼是鲸鱼？ 是，键入Y； 否，键入N：");
    answer = getchar(); getchar();
    printf("鲸鱼不是鱼。此题答案是：N\n");
    printf("你的答案对吗？正确键入1； 错误键入0：");
    YesorNot = getchar(); getchar();
    //赋值语句计算分数，补充在第26行
    if (YesorNot == '1') score++;
    printf("\n你答对了%d题，分数是%d分。\n",score,score);
    return 0;
}
```
使用两次getchar()的原因：
第一次为读取用户输入的字符，第二次为清除回车符\n。
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251017142637.png>)

# 实验作业03-顺序结构与选择结构
## T1
题目：
> 编写一个简单的计算器程序，用户输入两个整数，根据用户要求计算并输出他们的和、乘积、差、商和余数。

==解：==
```
#include <stdio.h>

int main()
{
    int a=1,b=1,c=1,d=1,e=1,g=1;
    double f;
    printf("请输入两个整数：");
    scanf("%d %d",&a,&b);
    c=a+b;
    d=a-b;
    e=a*b;
    f=(double)a/b;
    g=a%b;
    printf("两个数的和为%d\n",c);
    printf("两个数的差为%d\n",d);
    printf("两个数的积为%d\n",e);
    printf("两个数的商为%lf\n",f);
    printf("两个数的余数为%d\n",g);

    return 0;
}
```
运行结果如下：
![图片](</images/程序设计(A)(C)/Pasted_image_20251023110956.png>)

## T2
题目：
> 编写程序，读入 x (double)，按下式计算并输出 y（保留两位小数）。
![图片](</images/程序设计(A)(C)/Pasted_image_20251023111102.png>)

==解：==
```
#include <stdio.h>

int main()
{
    double x=0.0,y=0.0;
    printf("请输入x值：");
    scanf("%lf",&x);

    if(x<-1){y=-x;}
    else if( x>=-1 && x<=1 ){y=x*x;}
    else {y = 2*x + 1;}

    printf("y的值为%lf\n",y);

    return 0;
}
```
运行结果如下：
![图片](</images/程序设计(A)(C)/Pasted_image_20251023112135.png>)

## T3
题目：
> 编写程序，输入一个整数分数0-100，输出等级：\[90,100]→A, \[80,89]→B, \[70,79]→C, \[60,69]→D, \[0,59]→E ， 超出范围返回输入无效。

==解：==
```
#include <stdio.h>

int main()
{
    int score=0;
    char rank;
    printf("请输入一个整数分数0-100以给出评级：");
    scanf("%d",&score);
    if(score>100 || score<0){
        printf("请输入0-100的分数！");
        return 1;
    }
    else if(score>=90 && score<=100){
        rank = 'A';
    }
    else if(score>=80 && score<=89){
        rank = 'B';
    }
    else if(score>=70 && score<=79){
        rank = 'C';
    }
    else if(score>=60 && score<=69){
        rank = 'D';
    }
    else{
        rank = 'E';
    }
    printf("%c\n",rank);

    return 0;
}
```
运行结果如下：
![图片](</images/程序设计(A)(C)/Pasted_image_20251023114257.png>)

## T4
#零填充
题目：
> 编写程序，输入时、分、秒的三个整数（0≤h<24, 0≤m,s<60）。按 hh:mm:ss 输出，使用零填充：例如 03:07:09

==解：==
```C
#include <stdio.h>

int main()
{
    int h,m,s;
    printf("请输入时、分、秒的三个整数：");
    scanf("%d %d %d",&h,&m,&s);

    if(h >= 24 || h < 0 || m >= 60 || m < 0 || s >= 60 || s < 0){
        printf("请正确输入！\n");
        return 1;
    }
    printf("时间为%02d:%02d:%02d\n",h,m,s);

    return 0;
}
```
运行结果如下：
![图片](</images/程序设计(A)(C)/Pasted_image_20251023115514.png>)

## T5
> 编写程序，计算BMI：输入身高和体重（double），计算BMI = 体重 / (身高\*身高)，输出两行：第一行：BMI=数值（保留 1 位小数）；第二行：分类：<18.5: Underweight，18.5–23.9: Normal，24.0–27.9: Overweight，≥28.0: Obese。

==解：==
```C
#include <stdio.h>

int main()
{
    double h,w,BMI;
    char *rank;
    printf("请输入身高(m)和体重(kg)，中间用空格隔开：");
    scanf("%lf %lf",&h,&w);
    BMI = w / (h*h);
    
    if(BMI < 18.5){
        rank = "Underweight";
    }
    else if(BMI >= 18.5 && BMI <= 23.9){
        rank = "Normal";
    }
    else if(BMI >= 24.0 && BMI <= 27.9){
        rank = "Overweight";
    }
    else{
        rank = "Obese";
    }

    printf("BMI=%lf\n",BMI);
    printf("%s\n",rank);
    
    return 0;
}
```
运行结果如下：
![图片](</images/程序设计(A)(C)/Pasted_image_20251023131033.png>)

## T6
> 编写程序，用 getchar() 读取一个字符。若为小写字母，转换为对应大写并输出该字符；若为大写字母，转换为对应小写并输出该字符；其余情况输出other。

==解：==
```C
#include <stdio.h>

int main()
{
    char what;
    printf("请输入一个字符：");
    what = getchar();getchar();
    
    if(what >= 'a' && what <= 'z'){
        what = what - 32;
        printf("%c\n",what);
    }
    else if(what >= 'A' && what <= 'Z'){
        what = what + 32;
        printf("%c\n",what);
    }
    else{
        printf("Other");
    }

    return 0;
}
```
运行结果如下：
![图片](</images/程序设计(A)(C)/Pasted_image_20251023132033.png>)

# 实验作业04-程序流程控制
## T1 第几天
题目：
> 输入某年某月某日，判断这一天是这一年的第几天。

==解：==
```C
#include <stdio.h>

int main()
{
    int y=0, m=0, d=0, r=0;
    printf("请输入日期，格式为年/月/日，如2025/10/30：");
    scanf("%d/%d/%d", &y, &m, &d);
    switch (m) {
        case 12: r += 30;
        case 11: r += 31;
        case 10: r += 30;
        case 9: r += 31;
        case 8: r += 31;
        case 7: r += 30;
        case 6: r += 31;
        case 5: r += 30;
        case 4: r += 31;
        case 3: r += 28;
        case 2: r += 31;
        case 1: break;
        default:
            printf("月份有误\n");
            return 1;
    }
    r += d;
    printf("这是%d年的第%d天\n", y, r);

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251030133933.png>)

## T2 九九乘法表
题目：
> 按下面格式，输出九九乘法表：
> ![图片](</images/程序设计(A)(C)/Pasted_image_20251030134102.png>)

==解：==
```C
#include <stdio.h>

int main()
{
    int i, j, r;
    for (i = 1; i <= 9; i++) {
        for (j = 1; j <= i; j++) {
            printf("%d*%d=%d ", j, i, i * j);
        }
        printf("\n");
    }

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251030135605.png>)

## T3 GCD & LCM
题目：
> 编辑右边代码，测试并运行，写出测试用例及其执行截图，并说明程序功能。
> ![图片](</images/程序设计(A)(C)/Pasted_image_20251030135738.png>)

==解：==
编辑代码如下：
```C
#include <stdio.h>

int main()
{
    int m, n, r, t, temp;
    printf("please input 2 integers:");
    scanf("%d %d", &m, &n);
    t = m * n;
    if (m < n) {
        temp = m;
        m = n;
        n = temp;
    }
    while ((r = m % n) != 0) {
        m = n;
        n = r;
    }
    printf("%d,%d", n, t/n);

    return 0;
}
```
执行截图如下：
![图片](</images/程序设计(A)(C)/Pasted_image_20251030142143.png>)
程序功能说明：
这是一个运用辗转相除法计算最大公约数(GCD)和最小公倍数(LCM)的程序，最终输出结果中的前一个数即为GCD，后一个数即为LCM。

## T4 阶乘求和
题目：
> 编写程序，输入一个正整数 n，计算并输出 1!+2!+3!…+n! 。

==解：==
```C
#include <stdio.h>

int main()
{
    int i = 1, n = 1, f = 1, r = 0;
    printf("请输入一个正整数：");
    scanf("%d", &n);
    for (i = 1; i <= n; i++) {
        f = f * i;
        r += f;
    }
    printf("%d\n", r);

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251030143417.png>)

## T5 完数
题目：
> 如果一个整数的各个因子之和等于该数本身，如:6=1+2+3; 28=1+2+4+7+14,则 6 和 28 称为完数。编程输出 2~1000的所有完数。分别用while, do while,for三种循环语句实现。

==解：==
**用for循环**
```C
#include <stdio.h>

int main()
{
    int i, j, sum;
    for (i = 2; i <= 1000; i++) {
        sum = 0;

        for (j = 1; j < i; j++) {
            if (i % j == 0) {
                sum += j;}
        }
        
        if (sum == i) {
            printf("%d ", i);}
    }
    
    return 0;
}
```
**用while循环**
```C
#include <stdio.h>

int main()
{
    int i = 2, j, sum;
    while (i <= 1000) {
        sum = 0;
        j = 1;

        while (j < i) {
            if (i % j == 0) {
                sum += j;
            }
            j++;
        }

        if (sum == i) {
            printf("%d ", i);
        }

        i++;
    }
    
    return 0;
}
```
**用do while循环**
```C
#include <stdio.h>

int main()
{
    int i = 2, j, sum;
    do {
        sum = 0;
        j = 1;

        do {
            if (i % j == 0) {
                sum += j;
            }
            j++;
        } while (j < i);

        if (sum == i) {
            printf("%d ", i);
        }
        i++;
    }while (i <= 2000);

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251030151148.png>)

## T6 猜数游戏
题目：
> 编写一个交互式猜数游戏，程序随机生成一个 0～100 的整数。用户循环输入猜测的数：若偏大则输出“Too high”，偏小则输出“Too low”，猜中输出“Correct”。至多允许固定次数（如10次），猜中后提前结束。

```C
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    int key, guess, counts = 0, max = 10;

    srand(time(NULL));
    key = rand()%101;

    printf("===Guess Number===\n");
    printf("在%d次以内猜中我心中想的那个0~100的整数\n", max);

    while (counts < max){
        printf("第%d次猜测：", counts + 1);
        scanf("%d", &guess);
        if (guess > key) {
            printf("Too high\n");
        }
        else if (guess < key) {
            printf("Too low\n");
        }
        else {
            printf("Correct\n");
            break;
        }
        counts++;
    }
    if (counts == max) {
        printf("次数用光了，我想的数是%d", key);
    }

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251030153357.png>)

## T7 字符数量统计
题目：
> 输入一行字符，分类统计数字、英文字母、空格、其他字符各有多少。

==解：==
```C
#include <stdio.h>

int main() {
    int digits = 0, letters = 0, spaces = 0, others = 0;
    char ch;
    
    printf("请输入一行字符：\n");
    
    while ((ch = getchar()) != '\n') {
        if (ch >= '0' && ch <= '9') {
            digits++;
        }
        else if ((ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z')) {
            letters++;
        }
        else if (ch == ' ') {
            spaces++;
        }
        else {
            others++;
        }
    }
    
    printf("\n数字：%d\n", digits);
    printf("英文字母：%d\n", letters);
    printf("空格：%d\n", spaces);
    printf("其他字符：%d\n", others);
    
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251030155739.png>)

# 实验作业05-函数
## T1 GCD & LCM
题目：
> 编写程序，实现计算给定的两个int类型整数a和b的最大公约数的函数int gcd(int a, int b)和最小公倍数函数int lcm(int a, int b)

==解：==
```c
#include <stdio.h>

int gcd(int a, int b)
{
    while (b != 0) {
        int c = b;
        b = a % b;
        a = c;
    }
    return a;
}

int lcm(int a, int b)
{
    return a * b / gcd(a,b);
}

int main()
{
    int a = 1, b = 1;
    printf("请输入两个正整数：");
    scanf("%d %d", &a, &b);
    int gcd_result = gcd(a,b);
    int lcm_result = lcm(a,b);
    printf("最大公约数GCD为%d\n", gcd_result);
    printf("最小公倍数LCM为%d\n", lcm_result);
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251106211721.png>)

## T2 阶乘求和
题目：
> 编写程序，实现输入一个正整数n计算1!+2!+3!+...+n!的函数，其中int sum(int n)用于求和；int factor(int n)用于求阶乘

==解：==
```c
#include <stdio.h>

int factor(int n)
{
    int result_factor = 1, i = 1;
    for (i = 1; i <= n; i++) {
        result_factor *= i;
    }
    return result_factor;
}

int sum(int n)
{
    int result_sum = 0, i = 1;
    for (i = 1; i <= n; i++) {
        result_sum += factor(i);
    }
    return result_sum;
}

int main()
{
    int n = 1;
    printf("请输入整数n：");
    scanf("%d", &n);
    if (n <= 0) {
        printf("0");
    }
    else {
        printf("%d的阶乘求和结果为%d\n", n, sum(n));
    }
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251106213623.png>)

## T3 斐波那契递归
题目：
> 编写程序，实现计算第n个斐波那契数的函数int fib(int n)。fib(0)=0，fib(1)=1，fib(n)=fib(n-1)+fib(n-2)。

==解：==
```c
#include <stdio.h>

int fib(int n)
{
    if (n == 0) {
        return 0;}
    if (n == 1) {
        return 1;}
    if (n == -1) {
        return 1;}
    
    if (n > 1) {
        return fib(n - 1) + fib(n - 2);
    }
    else {
        return fib(n + 2) - fib(n + 1);
    }
}

int main()
{
    int n = 1;
    printf("请输入正整数n：");
    scanf("%d", &n);
    printf("第%d个斐波那契数为%d\n", n, fib(n));
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251106220129.png>)

## T4 判断质数
题目：
> 编写程序，实现计算判断正整数a是否为质数的函数int isPrime(int a)，输出1或者0，其中1表示是质数，0表示不是质数。

==解：==
```c
#include <stdio.h>

int isPrime(int a)
{
    if (a <= 1) {
        return 0;}
    if (a == 2) {
        return 1;}

    for (int i = 2; i < a; i++) {
        if (a % i == 0) {
            return 0;
        }
    }
    
    return 1;
}

int main()
{
    int a = 1;
    printf("请输入正整数a：");
    scanf("%d", &a);
    printf("%d\n", isPrime(a));
    
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251106221731.png>)

## T5 Binary_Differences
题目：
> 编写程序，实现计算给定的两个int类型整数a和b的二进制表示中有几位不同的函数int numDifferences(int a, int b)。使用异或计算。

==解：==
```c
#include <stdio.h>

int numDifferences(int a, int b)
{
    int xor_result = a ^ b;
    int count = 0;
    while (xor_result != 0) {
        if (xor_result & 1) {
            count ++;
        }
        xor_result = xor_result >> 1;
    }

    return count;
}

int main()
{
    int a, b;
    printf("请输入两个整数：");
    scanf("%d %d", &a, &b);
    printf("二进制表示中不同的位数为%d", numDifferences(a, b));

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251106230338.png>)

## T6 完美平方数
题目：
> 编写程序，实现计算给定的int类型整数n最少能由多少个完全平方数（1、4、9、16...）组成的函数int numSquares(int n)。基于拉格朗日四平方和定理任何正整数都可以表示为最多4个完全平方数的和。

==解：==
```c
#include <stdio.h>

int numSquares(int n)
{
    //检查本身
    for (int i = 1; i * i <= n; i++) {
        if (i * i == n) {
            return 1;
        }
    }

    //检查是否为2个完全平方数之和
    for (int i = 1; i * i <= n; i++) {
        int m = n - i * i;
        for (int j = 1; j * j <= m; j++) {
            if (j * j == m) {
                return 2;
            }
        }
    }

    //检查是否为3个完全平方数之和
    for (int i = 1; i * i <= n; i++) {
        for (int j = 1; j * j <= n; j++) {
            int m = n - i * i - j * j;
            for (int k = 1; k * k <= m; k++) {
                if (k * k == m) {
                    return 3;
                }
            }
        }
    }

    //其余为4
    return 4;
}

int main()
{
    int n = 1;
    printf("请输入一个正整数：");
    scanf("%d", &n);
    printf("%d最少能由%d个完全平方数表示\n", n, numSquares(n));

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251106232251.png>)


---
## T1_Revenge 去重排序
题目：
> 输入 n个数，对这 n个数去重之后排序，并输出从小到大排序结果 （先排序后去重）
> 测试说明
> 输入描述:
> 首先输入 n，然后接着输入n个数。其中1<=n<=108
> 输出描述:
> 输出去重之后从小到大排序结果（先排序后去重）
> 测试用例：
> 26 64 77 66 51 52 82 82 59 11 34 100 46 82 13 71 79 63 76 54 64 47 77 30 42 74 19

==解：==
```c
#include <stdio.h>

int main()
{
    int n = 1, i = 0, j = 0;
    int arr[108];
    printf("请输入n值：");
    scanf("%d", &n);
    printf("请输入%d个整数：", n);
    
    for (i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    for (i = 0; i < n; i++) {
        for (j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int k = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = k;
            }
        }
    }

    printf("去重排序后结果为：\n");
    for (i = 0; i < n; i++) {
        if (arr[i] != arr[i + 1]) {
            printf("%d ", arr[i]);
        }
    }
    printf("\n");

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251105192629.png>)

## T2_Revenge 最长连续长度
题目：
> 给定一个只有 0和1组成的数组，找出其中最长的连续1的长度。
> 测试说明
> 输入描述:
> 输入一个整数 n，表示有n个数字，其中 0<n<1000，数字仅为 0或1，接下来一行有 n个数字，表示数组的元素。
> 输出描述:
> 输出为一行，表示其中最长的连续 1的长度。
> 平台会对你编写的代码进行测试
> 测试输入:
> 9
> 100111011:
> 预期输出:
> 3

==解：==
```c
#include <stdio.h>

int main()
{
    int i = 0, n = 1;
    int arr[1000];
    int max = 0, current = 0;
    
    printf("请输入整数n：");
    scanf("%d", &n);
    printf("\n请输入%d个0或1：", n);
    for (i = 0; i < n; i++) {
        scanf("%1d", &arr[i]);
    }
    
    for (i = 0; i < n; i++) {
        if (arr[i] == 1) {
            current++;
            if (current > max) {
                max = current;
            }
        }
        else {
            current = 0;
        }
    }

    printf("最长连续1个数为%d", max);

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251105195134.png>)

# 实验作业06-变量的作用域生存期和一维数组
## T1 变量的作用域生存期
题目：
> 分析并写出下面程序的运行结果，理解变量的作用域和生存期。上传运行结果截图和你对该知识点的理解文字。

==解：==
```c
#include <stdio.h>
#include <stdlib.h>
int i=1;  void  other();
int main()
{   static int a;
    register int b=-10;
    int c=0;
    printf("---你的学号姓名---\n");
    printf("i:%d a:%d    "
      " b:%d c:%d\n",i,a,b,c);
    c=c+8;
    other();
    printf("-----Main------\n");
    printf("i:%d a:%d     "
         " b:%d c:%d\n",i,a,b,c);
    i=i+10;
    other(); 
    system("PAUSE");return 0;
}
void other()
{  static int a=2;
    static int b;
    int c=10;
    a=a+2;   i=i+32;  c=c+5;
    printf("-----Other------\n");
    printf("i:%d a:%d     "
        " b:%d c:%d\n",i,a,b,c);
    b=a;}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251115220703.png>)
我的理解：

| 存储类别     | 作用域 | 生存期       |
| -------- | --- | --------- |
| auto     | 局部  | 函数调用开始至结束 |
| register | 局部  | 函数调用开始至结束 |
| static局部 | 局部  | 程序整个运行期间  |
| static全局 | 全局  | 程序整个运行期间  |
| 全局       | 全局  | 程序整个运行期间  |

其中，最后一次进入`other()`时，由于`a`、`b`为静态的，故在上一次调用后其值保留，而局部`int c = 10`是重新创建并初始化为10的。

## T2 冒泡排序
题目：
> 输入一组数字，按由小到大输出结果。请用冒泡排序方法完成，并画出流程图（可以在纸上画，拍图上传）。参考教材例6-2.c,自查资料理解冒泡排序思路，上传流程图和程序代码。

==解：==
流程图如下：
<div class="mermaid">
graph TD;
    A(开始) --> B[输入 n];
    B --> C[输入 n 个数到数组 a];
    C --> D[i = 0];
    D --> E{i &lt; n - 1?};
    E -- 是 --> F[j = 0];
    E -- 否 --> M[输出排序后的数组 a];
    F --> G{j &lt; n - 1 - i?};
    G -- 是 --> H{a_j &gt; a_j1?};
    G -- 否 --> J[i = i + 1];
    H -- 是 --> I[交换 a_j 和 a_j1];
    H -- 否 --> K[不交换];
    I --> L[j = j + 1];
    K --> L;
    L --> F;
    J --> D;
    M --> N(结束);
</div>

代码如下：
```c
#include <stdio.h>

int main()
{
    int n;
    printf("请输入数的个数：");
    scanf("%d", &n);

    int arr[n];
    printf("请输入%d个整数：\n", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int t = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = t;
            }
        }
    }

    printf("冒泡排序后结果为：\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251115224527.png>)

## T3 合并排序
题目：
> 读下面程序，写结果，上传运行结果截图和对3个循环语句的功能理解的文字。

==解：==
```c
#include <stdio.h>
#define M 8
#define N 5

int main()
{
    int a[M] = {3,6,7,9,11,14,18,20};
    int b[N] = {1,2,13,15,17}, c[M+N];
    int i = 0, j = 0, k = 0;
    
    while(i < M && j < N) {
        if (a[i] < b[j]) {
            c[k] = a[i];
            i++;
            k++;
        } else {
            c[k] = b[j];
            j++;
            k++;
        }
    }
    
    while(i < M) {
        c[k] = a[i];
        i++;
        k++;
    }
    
    while(j < N) {
        c[k] = b[j];
        j++;
        k++;
    }
    
    for(i = 0; i < M + N; i++) {
        printf("%d ", c[i]);
    }
    
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251115225631.png>)
3个循环语句的功能理解：
1. 比较`a[i]`和`b[j]`中元素的大小并将较小者填入`c[k]`；
2. 若数组b已全部处理完而数组a还有剩余，则将a中剩余复制至c中；
3. 若数组a已全部处理完而数组b还有剩余，则将b中剩余复制至c中。

# 实验作业07-数组
## T1 斐波那契中偶数
题目：
> 将Fibonacci数列的前20项中的偶数找出来，并存放在一维数组中。

==解：==
```c
#include <stdio.h>

int main()
{
    int fib[20], evn[20];
    int count = 0;
    fib[0] = 1;
    fib[1] = 1;

    for (int i = 2; i < 20; i++) {
        fib[i] = fib[i - 1] + fib[i - 2];
    }
    for (int i = 0; i < 20; i++) {
        if (fib[i] % 2 == 0) {
            evn[count] = fib[i];
            count++;
        }
    }

    printf("Fibonacci数列中前20项分别为：\n");
    for (int i = 0; i < 20; i++) {
        printf("%d ", fib[i]);
    }
    printf("\n");
    printf("其中偶数有：\n");
    for (int i = 0; i < count; i++) {
        printf("%d ", evn[i]);
    }
    printf("\n");

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251120142654.png>)

## T2 选择排序
题目：
> 输入一组数字\[5, 7, 0, -3, 23]，按由小到大输出结果。请用选择排序方法完成。

> [!选择排序]
> 在第1~n个元素中找出最小值，把此元素与第1个元素交换；
> 在第2~n个元素中找出最小值，把此元素与第2个元素交换；
> ……
> 在第n-1~n个元素中找出最小值，把此元素与第n-1个元素交换；
> 最后一个值（第n个元素）必定是最大的。

==解：==
写了一个**稍加完善**版本的选择排序程序：
```c
#include <stdio.h>

void sort(int arr[], int n) {
    for (int i = 0; i < n -1; i++) {
        //找出最小值的索引
        int min_index = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[min_index]) {
                min_index = j;
            }
        }

        if (min_index != i) {
            int temp = arr[i];
            arr[i] = arr[min_index];
            arr[min_index] = temp;
        }
    }
}

void printarray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main()
{
    int n;
    printf("请输入数字个数：");
    scanf("%d", &n);
    printf("请输入%d个整数：\n", n);
    int a[n];
    for (int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
    }

    sort(a, n);
    printf("\n排序结果：\n");
    printarray(a, n);

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251120151404.png>)

## T3 T4 二维数组
题目：
> 3. 对下面的二维数组中的所有正数进行求和。
> 4. 将该二维数组中的各个元素的值按从小到大的顺序排列并重新输出。

$$\begin{bmatrix}
0  & -4 & 6 & 9 & 0\\
-6  & 4 & 0 & 7 & -5\\
-1  & 0 & 0 & 0 & 4\\
5  & -1 & -5 & 0 & 2\\
4  & 8 & 1 & -1 & 4
\end{bmatrix}$$

==解：==
```c
#include <stdio.h>

int a[5][5] = {{0, -4, 6, 9, 0},
               {-6, 4, 0, 7, -5},
               {-1, 0, 0, 0, 4},
               {5, -1, -5, 0, 2},
               {4, 8, 1, -1, 4}};

void T3(int arr[][5])
{
    int sum = 0;
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            if (arr[i][j] > 0) {
                sum += arr[i][j];
            }
        }
    }
    printf("正数求和为：%d\n", sum);
}

void T4(int arr[][5])
{
    int temp[25];
    int k = 0;

    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            temp[k] = arr[i][j];
            k++;
        }
    }

    //冒泡排序
    for (int i = 0; i < 25 - 1; i++) {
        for (int j = 0; j < 25 - 1 - i; j++) {
            if (temp[j] > temp[j + 1]) {
                int t = temp[j];
                temp[j] = temp[j + 1];
                temp[j + 1] = t;
            }
        }
    }

    printf("排序后数组为:\n");
    for (int i = 0; i < 25; i++) {
        printf("%d\t", temp[i]);
        if ((i + 1) % 5 == 0 && i < 24) {
            printf("\n");
        }
    }
    printf("\n");
}

int main()
{
    T3(a);
    T4(a);
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251120155718.png>)

## T5 strcmp()
题目：
> 输入5个字符串‘ABC’、‘123’、‘+-\*/’、‘\_hello’和‘ abc ’进行从小到大排序。使用strcmp函数实现并上传运行结果截图。

==解：==
```c
#include <stdio.h>
#include <string.h>

void sort(char str[][10], int n)
{
    char temp[10];
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (strcmp(str[j], str[j + 1]) > 0) {
                strcpy(temp, str[j]);
                strcpy(str[j], str[j + 1]);
                strcpy(str[j + 1], temp);
            }
        }
    }
}

void printStrings(char str[][10], int n)
{
    for (int i = 0; i < n; i++) {
        printf("%s\t", str[i]);
    }
    printf("\n");
}

int main()
{
    char strings[5][10] = {"ABC", "123", "+-*/", "_hello", " abc "};
    printf("原始字符串分别为:\n");
    printStrings(strings, 5);
    sort(strings, 5);
    printf("排序后为：\n");
    printStrings(strings, 5);
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251120163840.png>)

## T6 查找关键词
题目：
> 有5个预设的关键词，编程输入一行字符串，从前到后查找其中出现的关键单词（注意是单词不是字符）及出现次数。不用考虑部分重合的情况，比如关键字he与hear不匹配。

![图片](</images/程序设计(A)(C)/Pasted_image_20251120163942.png>)
==解：==
```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

//转小写
void toLower(char str[])
{
    int i = 0;
    while (str[i] != 0) {
        str[i] = tolower(str[i]);
        i++;
    }
}

//除标点
void stripPunct(char str[])
{
    int len = strlen(str);
    while (len > 0 && ispunct(str[len - 1])) {
        str[len - 1] = '\0';
        len--;
    }
}

int main()
{
    char keywords[5][20];
    int count[5] = {0};
    char text[1000];
    char word[20];

    printf("请输入5个关键词:\n");
    for (int i = 0; i < 5; i++) {
        scanf("%s", keywords[i]);
        toLower(keywords[i]);
    }

    getchar();    //处理换行符

    printf("请输入一串字符串:\n");
    fgets(text, 1000, stdin);

    int len = strlen(text);
    int i = 0;
    while (i <= len) {
        //提取单词
        int j = 0;
        while (i <= len && !isalnum(text[i])) {
            i++;    //跳过非字母数字
        }

        while (i <= len && isalnum(text[i]) && j < 20) {
            word[j++] = text[i++];
        }
        word[j] = '\0';

        if (j > 0) {
            stripPunct(word);
            toLower(word);

            //和关键词比较
            for (int k = 0; k < 5; k++) {
                if (strcmp(word, keywords[k]) == 0) {
                    count[k]++;
                }
            }
        }
    }

    printf("检索结果如下：\n");
    for (int i = 0; i < 5; i++) {
        printf("%s:%d\n", keywords[i], count[i]);
    }

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251120180917.png>)

## T7 反序输出
题目：
> 编写程序，实现字符串Hi,123@的反序输出。

==解：==
```c
#include <stdio.h>
#include <string.h>
#define MAX_LEN 1000

int main()
{
    char str[MAX_LEN];
    int len, i;

    printf("请输入一个字符串：\n");
    fgets(str, MAX_LEN, stdin);

    //去掉换行符
    len = strlen(str);
    if (len > 0 && str[len - 1] == '\n') {
        str[len - 1] = '\0';
        len--;
    }

    printf("原字符串：%s\n", str);
    printf("反序输出：");
    for (i = len - 1; i >= 0; i--) {
        printf("%c", str[i]);
    }
    printf("\n");

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251120183219.png>)

# 实验作业08-数组作为函数参数
## T1 折半查找
题目：
> 实现折半查找（二分查找）算法。
> 有10个数按从小到大的顺序存放在一个数组中。输入一个数,用二分法折半查找找出该数是这个数组中的第几个元素;如果不存在,显示“未找到”。
> 补全代码：
> ![图片](</images/程序设计(A)(C)/Pasted_image_20251127162037.png>)

==解：==
```c
int main() {
  int m[10] = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19}, key, KeyId;
  int search(int a[], int low, int high, int x);

  printf("please enter a number:");
  scanf("%d", &key);
  KeyId = search(m, 0, 9, key);
  if (KeyId == -1) {
    printf("\nsorry, not found");
  }
  else printf("\n%d is No.%d\n", key, KeyId + 1);

  return 0;
}

int search(int a[], int low, int high, int x) {
  if (low > high)
    return -1;

  int mid = (low + high) / 2;

  if (a[mid] == x)
    return mid;
  else if (a[mid] > x)
    return search(a, low, mid - 1, x);
  else
    return search(a, mid + 1, high, x);
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251127162340.png>)

## T2 自驾出游
题目：
> 实现自驾出游,计算驾驶时间。(输入,输出要求见课本例题6-15)

==解：==
```c
//自驾出游，计算驾驶时间

#include <stdio.h>
#define NTOWNS 5

void inputTimeTable(int time[][NTOWNS], char towns[][10], int n);
int selectCity(char towns[][10], int n);

void inputTimeTable(int time[][NTOWNS], char towns[][10], int n)
{
  for (int i = 0; i < n; i++) {
    time[i][i] = 0;
    for (int j = i + 1; j < n; j++) {
      printf("请输入%s至%s的驾驶时间：", towns[i], towns[j]);
      scanf("%d", &time[i][j]);
      time[j][i] = time[i][j];
    }
  }
}

int selectCity(char towns[][10], int n)
{
  int select, i;
  for (i = 0; i < n; i++) {
    printf("%d. %s\t", i, towns[i]);
  }
  printf("\n请输入将要出游的城市编号：");
  scanf("%d", &select);
  printf("你选择了%s\n", towns[select]);

  return select;
}

int main()
{
  char towns[NTOWNS][10] = {"武汉", "岳阳", "长沙", "南昌", "九江"};
  int timeTable[NTOWNS][NTOWNS];
  int city1, city2, city3;
  int time;

  printf("\n自驾出游，累计驾驶时间计算程序\n");
  printf("请输入旅行时间表\n");
  inputTimeTable(timeTable, towns, NTOWNS);

  city1 = selectCity(towns, NTOWNS);
  city2 = selectCity(towns, NTOWNS);
  city3 = selectCity(towns, NTOWNS);
  time = timeTable[city1][city2] + timeTable[city2][city3] + timeTable[city3][city1];

  printf("\n本次旅行驾驶时间总计%d\n", time);

  return 0;
}

```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251127171001.png>)

## T3 字符串处理函数
题目：
> 实现任意两个字符串处理函数。

==解：==
```c
#include <stdio.h>

//实现strcpy()
void my_strcpy(char *s1, const char *s2) {
    int i = 0;
    while ((s1[i] = s2[i]) != '\0') {
        i++;
    }
}

//实现strcmp()
int my_strcmp(const char *s1, const char *s2) {
    int i = 0;

    while (s1[i] == s2[i] && s1[i] != '\0') {
        i++;
    }

    return s1[i] - s2[i];
}

int main() {
    char a[100], b[100], c[100];

    printf("请输入字符串 a: ");
    scanf("%s", a);

    printf("请输入字符串 b: ");
    scanf("%s", b);

    my_strcpy(c, a);
    printf("\n使用 my_strcpy 后，c 的内容为: %s\n", c);

    int cmp = my_strcmp(a, b);

    printf("比较结果：");
    if (cmp == 0)
        printf("a 和 b 相等。\n");
    else if (cmp > 0)
        printf("a > b。\n");
    else
        printf("a < b。\n");

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251127183040.png>)

## T4 学生成绩
```c
#include <stdio.h>
#include <string.h>

#define MAX_STUDENTS 30
#define NAME_LENGTH 20
#define ID_LENGTH 15

// 定义学生结构体
typedef struct {
    char name[NAME_LENGTH];
    char id[ID_LENGTH];
    float programming_score;
    float math_score;
    float average_score;
} Student;

// 函数声明
void inputStudents(Student students[], int count);
void displayAllStudents(Student students[], int count);
void calculateAverages(Student students[], int count, float *class_prog_avg, float *class_math_avg);
void searchStudent(Student students[], int count, char *search_id);
void findTopStudents(Student students[], int count);

int main() {
    Student students[MAX_STUDENTS];
    int student_count;
    float class_prog_avg, class_math_avg;
    char search_id[ID_LENGTH];
    char choice;
    
    printf("请输入学生人数（最多%d人）：", MAX_STUDENTS);
    scanf("%d", &student_count);
    
    // 输入验证
    if (student_count <= 0 || student_count > MAX_STUDENTS) {
        printf("学生人数无效！\n");
        return 1;
    }
    
    // 输入学生信息
    inputStudents(students, student_count);
    
    // 计算个人平均分和班级课程平均分
    calculateAverages(students, student_count, &class_prog_avg, &class_math_avg);
    
    do {
        printf("\n========== 学生成绩管理系统 ==========\n");
        printf("1. 显示全班成绩表\n");
        printf("2. 查找学生信息\n");
        printf("3. 显示各科最高分学生信息\n");
        printf("4. 退出\n");
        printf("请选择操作（1-4）：");
        scanf(" %c", &choice);
        
        switch(choice) {
            case '1':
                // 显示全班成绩表
                displayAllStudents(students, student_count);
                printf("\n全班程序设计平均分：%.2f\n", class_prog_avg);
                printf("全班高等数学平均分：%.2f\n", class_math_avg);
                break;
                
            case '2':
                // 查找学生
                printf("请输入要查找的学生学号：");
                scanf("%s", search_id);
                searchStudent(students, student_count, search_id);
                break;
                
            case '3':
                // 显示各科最高分学生
                findTopStudents(students, student_count);
                break;
                
            case '4':
                printf("程序退出，谢谢使用！\n");
                break;
                
            default:
                printf("无效选择，请重新输入！\n");
        }
    } while(choice != '4');
    
    return 0;
}

// 输入学生信息
void inputStudents(Student students[], int count) {
    printf("\n请输入%d个学生的信息：\n", count);
    for(int i = 0; i < count; i++) {
        printf("\n学生 %d：\n", i + 1);
        printf("姓名：");
        scanf("%s", students[i].name);
        printf("学号：");
        scanf("%s", students[i].id);
        printf("程序设计成绩：");
        scanf("%f", &students[i].programming_score);
        printf("高等数学成绩：");
        scanf("%f", &students[i].math_score);
        
        // 输入验证
        if(students[i].programming_score < 0 || students[i].programming_score > 100 ||
           students[i].math_score < 0 || students[i].math_score > 100) {
            printf("成绩应在0-100之间，请重新输入！\n");
            i--;
        }
    }
}

// 显示所有学生信息
void displayAllStudents(Student students[], int count) {
    printf("\n%-5s %-15s %-10s %-12s %-12s %-10s\n", 
           "序号", "学号", "姓名", "程序设计", "高等数学", "平均分");
    printf("------------------------------------------------------------\n");
    
    for(int i = 0; i < count; i++) {
        printf("%-5d %-15s %-10s %-12.2f %-12.2f %-10.2f\n", 
               i + 1, 
               students[i].id, 
               students[i].name, 
               students[i].programming_score, 
               students[i].math_score, 
               students[i].average_score);
    }
}

// 计算平均分
void calculateAverages(Student students[], int count, float *class_prog_avg, float *class_math_avg) {
    float total_prog = 0, total_math = 0;
    
    for(int i = 0; i < count; i++) {
        // 计算个人平均分
        students[i].average_score = (students[i].programming_score + students[i].math_score) / 2.0;
        
        // 累加课程总分
        total_prog += students[i].programming_score;
        total_math += students[i].math_score;
    }
    
    // 计算班级课程平均分
    *class_prog_avg = total_prog / count;
    *class_math_avg = total_math / count;
}

// 查找学生
void searchStudent(Student students[], int count, char *search_id) {
    int found = 0;
    
    for(int i = 0; i < count; i++) {
        if(strcmp(students[i].id, search_id) == 0) {
            printf("\n找到学生信息：\n");
            printf("学号：%s\n", students[i].id);
            printf("姓名：%s\n", students[i].name);
            printf("程序设计成绩：%.2f\n", students[i].programming_score);
            printf("高等数学成绩：%.2f\n", students[i].math_score);
            printf("平均成绩：%.2f\n", students[i].average_score);
            found = 1;
            break;
        }
    }
    
    if(!found) {
        printf("未找到学号为 %s 的学生！\n", search_id);
    }
}

// 查找各科最高分学生
void findTopStudents(Student students[], int count) {
    if(count == 0) {
        printf("没有学生数据！\n");
        return;
    }
    
    // 查找程序设计最高分
    float max_prog = students[0].programming_score;
    int prog_top_index = 0;
    
    // 查找高等数学最高分
    float max_math = students[0].math_score;
    int math_top_index = 0;
    
    for(int i = 1; i < count; i++) {
        // 检查程序设计最高分
        if(students[i].programming_score > max_prog) {
            max_prog = students[i].programming_score;
            prog_top_index = i;
        }
        
        // 检查高等数学最高分
        if(students[i].math_score > max_math) {
            max_math = students[i].math_score;
            math_top_index = i;
        }
    }
    
    // 显示程序设计最高分学生
    printf("\n程序设计最高分学生信息：\n");
    printf("学号：%s，姓名：%s，成绩：%.2f\n", 
           students[prog_top_index].id, 
           students[prog_top_index].name, 
           students[prog_top_index].programming_score);
    
    // 显示高等数学最高分学生
    printf("高等数学最高分学生信息：\n");
    printf("学号：%s，姓名：%s，成绩：%.2f\n", 
           students[math_top_index].id, 
           students[math_top_index].name, 
           students[math_top_index].math_score);
}
```

## T5 指针理解
### T5-1
```c
#include <stdio.h>
#define PRT_ADDRESS

int main(int argc, char *argv[])
{
    int a, b, sum=0;
    printf("Please input two integers:");
    while (2 != scanf("%d%d", &a, &b)) {
        printf("\rPlease input two integers:");
        fflush(stdin);
    }
    sum = a + b;
    printf("\r%d+%d =%d", a, b, sum);

#ifdef PRT_ADDRESS
    printf("\r\nthe Addresses of argc and argc are %p and %p", &argc, argv);
    printf("\r\nthe Addresses of a, b, sum are %p, %p and %p", &a, &b, &sum);
    printf("\r\nthe Adresses of main, printf, scanf and fflush are %p,%p,%p and %p", main, printf, scanf, fflush);
#endif
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251127195708.png>)
### T5-2
```c
//计算课程的平均成绩和方差
#include <stdio.h>
#include <math.h>
#define MAX_NUM 6

int main()
{
    float score[MAX_NUM], average = 0, variance = 0, temp;
    int istep = 0;
    float *pscore = &score[0];
    while (istep < MAX_NUM) {
        printf("\rplease input a score:");
        scanf("%f", pscore);
        average += *pscore;
        pscore++;
        istep++;
    }
    istep = 0;
    pscore = &score[0];
    average = average / MAX_NUM;

    while (istep < MAX_NUM) {
        temp = *pscore - average;
        variance += temp * temp;
        pscore++;
        istep++;
    }
    variance /= MAX_NUM;
    variance = sqrt(variance);

    printf("\nAverage=%f, variance=%f\n", average, variance);
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251127202650.png>)
### T5-3
```c
#include <stdio.h>

void swapint(int *x, int *y)
{
    int temp;
    temp = *y;
    *y = *x;
    *x = temp;
}

int main(void)
{
    int a, b, *pa, *pb;
    pa = &a;
    pb = &b;
    printf("please input two integers:");
    scanf("%d%d", pa, pb);
    swapint(pa, pb);
    printf("a=%d, b=%d\n", a, b);
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251127204118.png>)

# 实验作业09-指针
## T1 最大最小值交换
题目：
> 编写void swapMinMax(int \*array);函数，计算数组中的最大值和最小值，并互换他们在数组中的所在位置

解：
```c
#include <stdio.h>

int size;

void swapMinMax(int *array)
{
    int minIndex = 0;
    int maxIndex = 0;
    int i = 0;

    for (i = 1; i < size; i++) {
        if (array[i] < array[minIndex])
            minIndex = i;
        if (array[i] > array[maxIndex])
            maxIndex = i;
    }

    int temp = array[minIndex];
    array[minIndex] = array[maxIndex];
    array[maxIndex] = temp;
}

int main()
{
    int arr[] = {5, 2, 8, 1, 9, 3};
    size = sizeof(arr) / sizeof(arr[0]);
    
    printf("交换前：");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }

    swapMinMax(arr);

    printf("\n交换后：");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251211144252.png>)

## T2 几月几日
题目：
> 编写void MonthDay(int year, int day, int \*pMonth, int \*pDay);函数，year表示年份（考虑闰年），day表示这一年的第几天，计算这一天是第几月第几日（比如12月12日）

解：
```c
#include <stdio.h>

int isLeapYear(int year)
{
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

void MonthDay(int year, int day, int *pMonth, int *pDay)
{
    int daysInMonth[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    if (isLeapYear(year))
        daysInMonth[1] = 29;
    
    int remaining = day;
    int month = 1;

    for (int i = 0; i < 12; i++) {
        if (remaining <= daysInMonth[i]) {
            month = i + 1;
            break;
        }
        remaining -= daysInMonth[i];
    }

    *pMonth = month;
    *pDay = remaining;
}

int main()
{
    int year, day, month, dayOfMonth;

    printf("请输入年份和天数：");
    scanf("%d", &year);
    scanf("%d", day);

    MonthDay(year, day, &month, &dayOfMonth);
    
    printf("%d年的第%d天是%d月%d日\n", year, day, month, dayOfMonth);

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251211150037.png>)

## T3 翻转数组中元素
题目：
> 翻转数组中的元素，编写reverse(int \*array, int len)函数，要求采用指针运算的方式，将array数组中的元素进行翻转（比如12345变为54321），要求不能改变array数组的首地址

解：
```c
#include <stdio.h>

void reverse(int *array, int len)
{
    int *left = array;
    int *right = array + len - 1;

    while (left < right) {
        int temp = *left;
        *left = *right;
        *right = temp;
        left++;
        right--;
    }
}

int main()
{
    int len;
    printf("请输入数组长度：");
    scanf("%d", &len);
    int array[len];

    printf("请输入%d个整数：\n");
    for (int i  = 0; i < len; i++) {
        scanf("%d", &array[i]);
    }
    printf("\n首元素地址为%p\n", array);

    reverse(array, len);

    printf("翻转后：\n");
    for (int i = 0; i < len; i++) {
        printf("%d ", array[i]);
    }
    printf("\n首元素地址为%p\n", array);
    
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251211151234.png>)

## T4 升序数组合并
题目：
> 已知两个分别按升序排序的整型数组 a 和 b，长度分别为 n 和 m，请实现函数，将它们合并到一个新的升序数组 c 中（长度为 n + m），在实现中使用两个指针分别指向 a 与 b 的当前位置，比较大小后移动对应指针并写入到 c 中，同时要求整个过程中尽量避免使用下标形式访问，而是通过指针加减和解引用完成遍历与赋值，并在最后返回合并后数组的指针。

解：
```c
#include <stdio.h>

void merge(int *a, int n, int *b, int m, int *c)
{
    int *pa = a;
    int *pb = b;
    int *pc = c;

    int *a_end = a + n;
    int *b_end = b + m;

    while (pa < a_end && pb < b_end) {
        if (*pa <= *pb) {
            *pc = *pa;
            pa++;
        }
        else {
            *pc = *pb;
            pb++;
        }
        pc++;
    }

    while (pa < a_end) {
        *pc = *pa;
        pa++;
        pc++;
    }

    while (pb < b_end) {
        *pc = *pb;
        pb++;
        pc++;
    }
}

void printArray(int *arr, int len)
{
    int *p = arr;
    int *end = arr + len;
    while (p < end) {
        printf("%d ", *p);
        p++;
    }
    printf("\n");
}

int main()
{
    int n, m;
    printf("请输入升序数组a的长度：");
    scanf("%d", &n);
    int a[n];
    printf("请向数组a中输入%d个元素：\n", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
    }
    printf("请输入升序数组b的长度：");
    scanf("%d", &m);
    int b[m];
    printf("请向数组a中输入%d个元素：\n", m);
    for (int i = 0; i < m; i++) {
        scanf("%d", &b[i]);
    }

    int c[m + n];
    merge(a, n, b, m, c);
    printf("合并后：\n");
    printArray(c, m + n);

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251211153811.png>)

## T5 malloc动态分配内存
题目：
> 请编写一个程序，从键盘读入一个正整数 n，使用 malloc 动态分配一块可以存放 n 个 int 的连续空间，然后再从键盘读入这 n 个整数存入该动态数组中。接下来，使用指针（如 int \*p = arr; p++、\*p 的形式）遍历这段内存，找出数组中的最大值并输出.

解：
```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
    int n;

    printf("请输入正整数n：");
    scanf("%d", &n);

    if (n <= 0) {
        printf("请输入正整数n\n");
        return 1;
    }

    int *arr = malloc(n * sizeof(int));
    if (arr == NULL) {
        printf("内存分配失败\n");
        return 1;
    }

    printf("请输入%d个整数：\n", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    int *p = arr;
    int *end = arr + n;
    int max = *p;

    while (p < end) {
        if (*p > max)
            max = *p;
        p++;
    }

    printf("数组中最大值为%d\n", max);

    free(arr);

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251211155210.png>)

## T6 星期
题目：
> 编写一个程序，输入星期（数字），输出该星期的英文名。
> （要求：用指针数组处理。）

解：
```c
#include <stdio.h>

int main()
{
    char *weekdays[] = {
        "Sunday", "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday"
    };
    
    int day;

    printf("请输入星期数字(0-6，0表示周日)：\n");
    scanf("%d", &day);

    if (day < 0 || day > 6)
        printf("输入错误\n");
    else
        printf("其英文名是%s\n", weekdays[day]);

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251211160444.png>)


## T7 通用排序函数
题目：
> 使用函数指针，编写对数组array进行排序的通用函数void sort(int \*array, int len, int(\*sortType)(int type))，要求type表示不同的排序算法（比如，0表示选择排序，1表示插入排序，2表示冒泡排序）

解：
```c
#include <stdio.h>

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

// 选择排序
void selectionSort(int *array, int len)
{
    for (int i = 0; i < len - 1; i++) {
        int minIndex = i;
        for (int j = i + 1; j < len; j++) {
            if (array[j] < array[minIndex])
                minIndex = j;
        }
        if (minIndex != i)
            swap(&array[i], &array[minIndex]);
    }
}

// 插入排序
void insertionSort(int *array, int len)
{
    for (int i = 1; i < len; i++) {
        int key = array[i];
        int j = i - 1;
        while (j >= 0 && array[j] > key) {
            array[j + 1] = array[j];
            j--;
        }
        array[j + 1] = key;
    }
}

// 冒泡排序
void bubbleSort(int *array, int len)
{
    for (int i = 0; i < len - 1; i++) {
        for (int j = 0; j < len - 1 - i; j++) {
            if (array[j] > array [j + 1])
                swap(&array[j], &array[j + 1]);
        }
    }
}

int sortType(int type)
{
    if (type >= 0 && type <= 2)
        return type;
    return -1;
}

void sort(int *array, int len, int (*sortType)(int type), int type)
{
    int choose = sortType(type);
    if (choose == 0)
        selectionSort(array, len);
    else if (choose == 1)
        insertionSort(array, len);
    else if (choose== 2)
        bubbleSort(array, len);
    else
        printf("输入错误\n");
}
```

# 实验作业10-结构体与链表
## T1 学习链表

题目：
> 对照书例8-5、例8-6、例8-7，输入代码，理解本章知识点。

解：
```c
#include <stdio.h>
#include <stdlib.h>
struct link *AppendNode(struct link *head);
void DisplyNode(struct link *head);
void DeleteMemory(struct link *head);
struct link
{
    int data;
    struct link *next;
};
int main(void)
{
    int i = 0;
    char c;
    struct link *head = NULL; // 链表头指针
    printf("Do you want to append a new node(Y/N)?");
    scanf(" %c", &c); // 前有一个空格
    while (c == 'Y' || c == 'y')
    {
        head = AppendNode(head);
        DisplyNode(head); // 显示当前链表中各结点信息
        printf("Do you want to append a new node(Y/N)?");
        scanf(" %c", &c);
        i++;
    }
    printf("%d new nodes have been apended!\n", i);
    DeleteMemory(head); // 释放所有动态分配的内存
}
// 函数功能：新建一个结点并添加到链表末尾，返回添加结点后链表的头指针
struct link *AppendNode(struct link *head)
{
    struct link *p = NULL, *pr = head;
    int data;
    p = (struct link *)malloc(sizeof(struct link)); // 让 p 指向新建结点
    if (p == NULL)
    {
        printf("No enough memory to allocate!\n");
        exit(0);
    }
    if (head == NULL) // 若原链表为空，则将新建结点置为首结点
    {
        head = p;
    }
    else // 若原链表为非空，则将新建结点添加到表尾
    {
        while (pr->next != NULL) // 若未到表尾，则移动 pr 直到 pr 指向表尾
        {
            pr = pr->next; // 让 pr 指向下一个结点
        }
        pr->next = p; // 将新建结点添加到链表的末尾
    }
    pr = p; // 让 pr 指向新结点
    printf("Input node data:");
    scanf("%d", &data); // 输入结点数据
    pr->data = data;
    pr->next = NULL; // 将新建结点置为表尾
    return head; // 返回添加结点后的链表的头结点指针
}
// 函数功能：显示链表中所有结点的结点号和该节点中数据项内容
void DisplyNode(struct link *head)
{
    struct link *p = head;
    int j = 1;
    while (p != NULL) // 若不是表尾，则循环打印
    {
        printf("%5d%10d\n", j, p->data); // 打印第 j 个结点的数据
        p = p->next;
        j++;
    }
}
// 函数功能：释放 head 指向的链表中所有节点占用的内存
void DeleteMemory(struct link *head)
{
    struct link *p = head,  *pr = NULL;
    while (p != NULL) // 若不是表尾，则释放结点占用的内存
    {
        pr = p; // 在 pr 中保存当前结点的指针
        p = p->next; // 让 p 指向下一个结点
        free(pr); // 释放 pr 指向的当前结点占用的内存
    }
}
// 从 head 指向的链表中删除一个结点，返回删除结点后的链表的头指针
struct link *DeleteNode(struct link *head, int nodeData)
{
    struct link *p = head, *pr = head;
    if (head == NULL) // 若链表为空，则退出程序
    {
        printf("Linked Table is empty!\n");
        return (head);
    }
    while (nodeData != p->data && p->next != NULL) // 未找到且未到尾
    {
        pr = p;
        p = p->next;
    }
    if (nodeData == p->data) // 若找到结点 nodeData，则删除该结点
    {
        if (p == head) // 若待删除结点为首结点，则 head 指向第二个结点
        {
            head = p->next;
        }
        else // 不是首结点，则将上一个结点的指针指向当前结点的下一个结点
        {
            pr->next = p->next;
        }
        free(p); // 释放内存
    }
    else // 没有找到待删除结点
    {
        printf("This Node has not been found!\n");
    }
    return head; // 返回头结点指针
}
// 在已按升序排序的链表中插入一个结点，返回插入结点后的链表头指针
struct link *InsertNode(struct link *head, int nodeData)
{
    struct link *pr = head, *p = head, *temp = NULL;
    p = (struct link *)malloc(sizeof(struct link)); // 让 p 指向待插入结点
    if (p == NULL) // 若申请内存失败，则退出程序
    {
        printf("No enough memory!\n");
        exit(0);
    }
    p->next = NULL; // 为待插入结点的指针域赋值为空指针
    p->data = nodeData; // 为待插入结点的数据域赋值为 nodeData
    if (head == NULL) // 若原链表为空表
    {
        head = p; // 待插入结点作为头结点
    }
    else
    {
        // 若未找到待插入结点的位置且未到表尾，则继续找
        while (pr->data < nodeData && pr->next != NULL)
        {
            temp = pr; // 在 temp 中保存当前结点的指针
            pr = pr->next; // pr 指向当前结点的下一个结点
        }
        if (pr->data >= nodeData)
        {
            if (pr == head) // 若在头结点前插入新结点
            {
                p->next = head; // 将新结点的指针域指向原链表的头结点
                head = p; // 让 head 指向新结点
            }
            else
            {
                pr = temp;
                p->next = pr->next; // 让新结点的指针域指向下一个结点
                pr->next = p;       // 让上一个结点的指针域指向新结点
            }
        }
        else // 若在表尾插入新结点
        {
            pr->next = p; // 让末结点的指针域指向新结点
        }
    }
    return head; // 返回头指针
}
```

## T2 头插法尾插法创建链表

题目：
> 分别用尾插法和头插法创建单链表，并打印单链表。

解：
```c
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *next;
};

void printList(struct Node *head)
{
    struct Node *p = head;
    if (p == NULL) {
        printf("链表为空！\n");
    }
    printf("链表内容：");
    while (p != NULL) {
        printf("%d ", p->data);
        p = p->next;
    }
    printf("\n");
}

// 头插法创建链表
struct Node *createListByHead()
{
    struct Node *head = NULL;
    int x;
    printf("请输入整数（头插法，输入 -1 结束）：");
    while (scanf("%d", &x) == 1 && x != -1) {
        struct Node *newNode = (struct Node *)malloc(sizeof(struct Node));
        if (newNode == NULL) {
            printf("内存分配失败！\n");
            exit(1);
        }
        newNode->data = x;
        newNode->next = head; // 新结点指向当前头结点
        head = newNode; // 更新头指针
    }
    return head;
}

// 尾插法创建链表
struct Node *createListByTail()
{
    struct Node *head = NULL;
    struct Node *tail = NULL;
    int x;
    printf("请输入整数（尾插法，输入 -1 结束）：");
    while (scanf("%d", &x) == 1 && x != -1) {
        struct Node *newNode = (struct Node *)malloc(sizeof(struct Node));
        if (newNode == NULL) {
            printf("内存分配失败！\n");
            exit(1);
        }
        newNode->data = x;
        newNode->next = NULL;

        if (head == NULL) {
            head = tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
    }
    return head;
}

// 释放内存
void freeList(struct Node *head)
{
    struct Node *temp;
    while (head != NULL) {
        temp = head;
        head = head->next;
        free(temp);
    }
}

// 主函数：展示
int main()
{
    struct Node *list1, *list2;

    printf("头插法创建链表\n");
    list1 = createListByHead();
    printList(list1);
    free(list1);

    printf("尾插法创建链表\n");
    list2 = createListByTail();
    printList(list2);
    free(list2);

    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251218172205.png>)

## T3 删除指定结点

题目：
> 删除指定（分别按位置和值指定）结点。

解：
```c
// 按位置删除结点
struct Node *deleteByPos(struct Node *head, int pos)
{
    if (head == NULL || pos < 1) {
        printf("链表为空或位置无效。\n");
        exit(1);
    }

    struct Node *temp = head;

    if (pos == 1) {
        head = head->next;
        free(temp);
        return head;
    }
    for (int i = 1; i < pos - 1; i++) {
        temp = temp->next;
        if (temp == NULL || temp->next == NULL) {
            printf("超出长度。\n");
            return head;
        }
    }
    struct Node *p = temp->next;
    temp->next = p->next;
    free(p);
    return head;
}

// 按值删除结点
struct Node *deleteByVal(struct Node *head, int val)
{
    if (head == NULL) {
        printf("链表为空。\n");
        return head;
    }

    struct Node *temp = head;
    struct Node *p = head;

    while (p->data != val && p->next != NULL) {
        temp = p;
        p = p->next;
    }
    if (p->data == val) {
        if (p == head) {
            head = p->next;
        } else {
            temp->next = p->next;
        }
        free(p);
    } else {
        printf("未找到。\n");
    }
    return head;
}
```

## T4 单链表逆序

题目：
> 单链表逆序并输出。

解：
```c
// 单链表逆序：让每个箭头掉头
struct Node *reverseList(struct Node *head)
{
    struct Node *prev = NULL;
    struct Node *curr = head;
    struct Node *next = NULL;

    while (curr != NULL) {
        next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }

    return prev;
}

// 主函数：展示
int main()
{
    printf("创建原链表:\n");
    struct Node *list = createListByTail();
    printf("原链表: ");
    printList(list);

    list = reverseList(list);
    printf("反转后: ");
    printList(list);

    freeList(list);
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251218181628.png>)

## T5 单增链表合并

题目：
> 输入两个单调递增的链表，输出两个链表合成后的链表，同时要求合成后的链表依然保持递增排序。

解：
```c
// 合并单增链表
struct Node *mergeLists(struct Node *list1, struct Node *list2)
{
    struct Node head; // 创建一个空的结点作为标杆
    struct Node *tail = &head;
    while (list1 && list2) {
        if (list1->data <= list2->data) {
            tail->next = list1;
            list1 = list1->next;
        } else {
            tail->next = list2;
            list2 = list2->next;
        }
        tail = tail->next;
    }
    tail->next = list1 ? list1 : list2;
    return head.next;
}

// 主函数：展示
int main()
{
    printf("创建第一个递增链表：\n");
    struct Node *list1 = createListByTail();
    printf("创建第二个递增链表：\n");
    struct Node *list2 = createListByTail();
    printf("合并后链表：");
    struct Node *merged = mergeLists(list1, list2);
    printList(merged);
    freeList(merged);
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251218184433.png>)

## T6 链表分区

题目：
> 给你一个链表的头节点 head 和一个特定值 x ，请你对链表进行分隔，使得所有 小于 x 的节点都出现在 大于或等于 x 的节点之前。你不需要 保留 每个分区中各节点的初始相对位置。

解：
```c
// 链表分区
struct Node *partition(struct Node *head, int x)
{
    struct Node smaller = {0, NULL};
    struct Node greater = {0, NULL};
    struct Node *smallerTail = &smaller;
    struct Node *greaterTail = &greater;
    struct Node *curr = head;

    while (curr != NULL) {
        struct Node *next = curr->next; // 保存下一个结点
        curr->next = NULL; // 断开此结点的 next 避免成环
        if (curr->data < x) {
            smallerTail->next = curr;
            smallerTail = curr;
        } else {
            greaterTail->next = curr;
            greaterTail = curr;
        }
        curr = next;
    }

    smallerTail->next = greater.next;
    return smaller.next;
}

// 主函数：展示
int main()
{
    int x;
    printf("创建原链表：");
    struct Node *list = createListByTail();
    printf("输入分区值 x ：");
    scanf("%d", &x);
    printf("链表分区后：");
    partition(list, x);
    printList(list);
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251218192805.png>)

## T7 约瑟夫问题

题目：
> 编号为 1 到 n 的 n 个人围成一圈。从编号为 1 的人开始报数，报到 m 的人离开。下一个人继续从 1 开始报数。n-1 轮结束以后，只剩下一个人，问最后留下的这个人编号是多少？（用单向循环链表来实现）

解：
```c
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *next;
};

struct Node *circle(int n)
{
    if (n <= 0)
        return NULL;

    struct Node *head = (struct Node *)malloc(sizeof(struct Node));
    head->data = 1;
    head->next = head;

    struct Node *temp = head;
    for (int i = 2; i <= n; i++) {
        struct Node *newNode = (struct Node *)malloc(sizeof(struct Node));
        newNode->data = i;
        newNode->next = head; // 成环
        temp->next = newNode;
        temp = newNode;
    }
    return head;
}

int josephus(int n, int m)
{
    if (n <= 0 || m <= 0)
        return -1;
    if (n == 1)
        return 1;

    struct Node *head = circle(n);
    struct Node *curr = head;
    struct Node *prev = NULL;

    while (curr->next != head) {
        curr = curr->next;
    }
    prev = curr; // prev 指向 head 前一个结点
    curr = head; // curr 指向 head

    // 还需 n-1 次循环
    for (int round = 0; round < n - 1; round++) {
        // 移动 m-1 步
        for (int count = 1; count < m; count++) {
            prev = curr;
            curr = curr->next;
        }
        // 删除
        printf("%d离开\n", curr->data);
        prev->next = curr->next;
        struct Node *p = curr;
        curr = curr->next;
        free(p);
    }

    int last = curr->data;
    free(curr);
    return last;
}

int main()
{
    int n, m;
    printf("请输入人数 n 和报数 m：");
    scanf("%d %d", &n, &m);

    int last = josephus(n, m);
    printf("最后剩下的人的编号为%d\n", last);
    return 0;
}
```
运行结果如图：
![图片](</images/程序设计(A)(C)/Pasted_image_20251218195058.png>)
