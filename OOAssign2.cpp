/* 
 * File:   main.cpp
 * Author: Sam
 *
 * Created on February 11, 2019, 7:32 PM
 */

#include <cstdlib>
#include <iostream>

using namespace std;

/*
 * 
 */

class Shape{//Top class, represents all shapes
    public:
        string type = "undefined";
        int order;//Order represents the order in which the object should be 'displayed' (1 is first, etc)
        Shape(){//default constructor, not used
            order=-1;
        }
        Shape(int ordin){//Sets order to input
            order=ordin;
        }
        void identify(){
            cout<<"I am a "<<type<<" in position "<<order<<endl;
        }
};

class Square: public Shape{//Square inherits Shape
public:
    Square(int ordtwo):Shape(ordtwo){//Overloaded constructor calls Shape constructor
        type = "square";
    }
};

class Triangle: public Shape{
public:
    Triangle(int ordtwo):Shape(ordtwo){
        type = "triangle";
    }
};

class Circle: public Shape{
public:
    Circle(int ordtwo):Shape(ordtwo){
        type = "circle";
    }
};

int main(int argc, char** argv) {
    Circle shape1 = Circle(1);//Don't know how to make a list of objects
    Square shape2 = Square(2);
    Square shape3 = Square(3);
    Triangle shape4 = Triangle(4);
    shape1.identify();//All shapes just call identify with varying output
    shape2.identify();
    shape3.identify();
    shape4.identify();
    return 0;
}

