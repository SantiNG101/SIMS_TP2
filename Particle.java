public class Particle {
    private double x, y, theta;

    public Particle(double x, double y, double theta) {
        this.x = x;
        this.y = y;
        this.theta = theta;
    }

    public double getX(){
        return x;
    }

     public double getY(){
        return y;
    }

     public double getTheta(){
        return theta;
    }

    public void setX(double x){
        this.x=x;
    }

     public void setY(double y){
        this.y=y;
    }

     public void setTheta(double theta){
        this.theta=theta;
    }

    public double vx(double v) { return v * Math.cos(theta); }
    public double vy(double v) { return v * Math.sin(theta); }
}
