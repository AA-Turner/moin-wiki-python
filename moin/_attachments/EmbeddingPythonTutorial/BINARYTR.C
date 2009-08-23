#include<stdio.h>
#include<stdlib.h>
#include<conio.h>
#include<malloc.h>
typedef struct treenode *position;
typedef struct treenode *searchtree;
position findpos(int ,searchtree);
position findmin(searchtree);
position findmax(searchtree);
searchtree insert(int ,searchtree );
searchtree del(int,searchtree);
void display( searchtree);
struct treenode
{
 int ele;
 searchtree right;
 searchtree left;
}*t,*temp;

void main()
{
int x,ch,*tp;
clrscr();

do
{
 printf("\n1.Insert\n2.Delete\n3.Findposition\n4.Findmin");
 printf("\n5.Findmax\n6.Display\n7.exit ");
 printf("\nEnter ur choice:");
 scanf("%d",&ch);
 switch(ch)
 {
  case 1:printf( "Enter the data");
	 scanf("%d",&x);
	 t=insert(x,t);
	 break;

  case 2:printf("Enter the data to be deleted");
	 scanf("%d",&x);
	 t= del(x,t);
	 break;

  case 3:printf("\nEnter the element to find its position");
	 scanf("%d",&x);
	 temp=findpos(x,t);
	 if(x==temp->ele)
	 printf("\nthe element is in the tree");
	 else
	 printf("the element is not in the tree");
	 break;

  case 4:temp=findmin(t);
	 printf("the min element is :%d",temp->ele);
	 break;

  case 5:temp=findmax(t);
	 printf("\nthe max element is :%d ",temp->ele);
	 break;

  case 6:display(t);
	 break;

  case 7:exit(0);
	 break;
  }

}while(ch!=7);

getch();

}

searchtree insert(int x,searchtree t)
{
  if(t==NULL)
  {
     t=(struct treenode*)malloc(sizeof(struct treenode));
       if(t==NULL)
	 printf("\nout of space");
       else
       {
	 t->ele=x;
	 t->left=NULL;
	 t->right=NULL;
       }
  }

     if(x<t->ele)
	 t->left=insert(x,t->left);
     else if(x>t->ele)
	 t->right=insert(x,t->right);
     return t;
}

searchtree del(int x,searchtree t)
{
    position tmpcell;
    if(t==NULL)
      printf("Element not found");
    else if(x<t->ele)
      t->left=del(x,t->left);
    else if(x>t->ele)
      t->right=del(x,t->right);
    else if(t->left&&t->right)
    {
      tmpcell=t;
      tmpcell=findmin(t->right);
      t->ele=tmpcell->ele;
      t->right=del(t->ele,t->right);
    }
    else
    {
    tmpcell=t;
    if(t->left==NULL)
     t=t->right;
    else if(t->right==NULL)
     t=t->left;
     free(tmpcell);
    }
    return t;
}
position findpos(int x,searchtree t)
{
    if(t==NULL)
      return NULL;
    else if(x<t->ele)
      return findpos(x,t->left);
    else if(x>t->ele)
      return findpos(x,t->right);
    else
      return t;
}
position findmin(searchtree t)
{
    if(t==NULL)
      return NULL;
    else if(t->left==NULL)
      return t;
    else
      return findmin(t->left);
}
position findmax(searchtree t)
{
    if(t==NULL)
      return NULL;
    else if(t->right==NULL)
      return t;
    else
      return findmax(t->right);
}
void display(searchtree t)
{

    if(t!=NULL)
    {
      display(t->left);
      printf("\n%d",t->ele);
      display(t->right);
    }
}