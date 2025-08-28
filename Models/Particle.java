package Models;

public class Particle {
    private double x, y, theta;
    private final int id;
    private double c,s;
    private int count;

    public Particle(double x, double y, double theta, int id) {
        this.x = x;
        this.y = y;
        this.theta = theta;
        this.id = id;
        this.count = 0;
    }

    public int getId() { return id; }
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

    public void registerCloseParticle(Particle p) {
        c += Math.cos(p.getTheta());
        s += Math.sin(p.getTheta());
        count += 1;
    }
    public static void registerCloseParticles(Particle p1, Particle p2){ //! suma atomica
        p1.registerCloseParticle(p2);
        p2.registerCloseParticle(p1);
    }

    public double getMeanAngle () {
        return Math.atan2(s/count, c/count);
    }

    public void resetMeanAngle() {
        c = 0.0;
        s = 0.0;
        count = 0;
    }

    public double vx(double v) { return v * Math.cos(theta); }
    public double vy(double v) { return v * Math.sin(theta); }
}
