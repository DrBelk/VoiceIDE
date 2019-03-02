#include <QPainter>

class car
{

protected:
    float x;
    float y;
    float vx;
    float vy;
    float width;
    float height;
    float scale;
    float max_speed;

public:
    car();
    car(float new_x, float new_y, float new_vx, float new_vy, float new_width, 
        float new_height, float new_scale, float new_max_speed);

    void show(QPainter &qp);

    //перенес из car_user, т.к. использую и в автоматической машинке
    void move_forward();
    void move_back();
    void inertia();
    void turn_left();
    void turn_right();
    void turn();
    void move();

};

car::car() {
    x = y = 0;
    vx = vy = 0;
    width = 20;
    height = 44;
    max_speed = 50;
    scale = 0;
}

car::car(float new_x, float new_y, float new_vx, float new_vy, float new_width, float new_height, float new_scale, float new_max_speed) {
     x = new_x;
     y = new_y;
     vx = new_vx;
     vy = new_vy;
     width = new_width;
     height = new_height;
     scale = new_scale;
     max_speed = new_max_speed;
    }

void car::show(QPainter &pt)
    {pt.translate(x, y);
     pt.rotate(-scale);
     pt.drawPixmap(-width/2, -height/2,width,height,QPixmap("texture/1.png"));
     pt.restore();
    }

//Перенесенные функции движения
//Движение:

void car::move()
{
    x += c*vx;
    y += c*vy;
}

//Движение вперёд:

void car::move_forward()
{if(sqrt(pow(vx,2) + pow(vy,2)) <= max_speed)
    {vx -= sin(scale*3.14159265359/180);
        vy -= cos(scale*3.14159265359/180);
    }
}

//Движение назад:

void car::move_back()
{if(sqrt(pow(vx,2) + pow(vy,2)) <= max_speed)
    {vx += sin(scale*3.14159265359/180);
        vy += cos(scale*3.14159265359/180);
    }
}

//Торможение при повороте:

void car::turn()
{if(vx > 0)
        vx -= 0.5;
    else
        if(vx < 0)
            vx += 0.5;
    if(vy > 0)
        vy -= 0.5;
    else
        if(vy < 0)
            vy += 0.5;
}

//Поворот влево:

void car::turn_left()
{if(sqrt (pow(vx,2) + pow(vy,2)) > 0)
    {this->turn();
        scale += 1.5;
    }
}

//Поворот вправо:

void car::turn_right()
{if(sqrt (pow(vx,2) + pow(vy,2)) > 0)
    {this->turn();
        scale -= 1.5;
    }
}

//Движение по инерции:

void car::inertia()
{if(floor(sqrt(pow(vx,2) + pow(vy,2))) == 0)
        vx = vy = 0;
    else
    {if(vx > 0){
            vx -= stop_c*fabs(sin(scale*3.14159265359/180));
            //vx -= stop_c*fabs(cos(scale*3.14159265359/180));
        }
        else
            if(vx < 0){
                vx += stop_c*fabs(sin(scale*3.14159265359/180));
                //vx += stop_c*fabs(cos(scale*3.14159265359/180));
            }
        if(vy > 0)
        {//vy -= stop_c*fabs(sin(scale*3.14159265359/180));
            vy -= stop_c*fabs(cos(scale*3.14159265359/180));
        }
        else
            if(vy < 0){
                // vy += stop_c*fabs(sin(scale*3.14159265359/180));
                vy += stop_c*fabs(cos(scale*3.14159265359/180));
            }
    }
}
