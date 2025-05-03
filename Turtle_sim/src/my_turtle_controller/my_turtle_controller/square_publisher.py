import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # Import the Twist message type
import math

class SquarePublisherNode(Node):
    def __init__(self):
        super().__init__('square_publisher') # Node name
        # Create a publisher:
        # takes message type, topic name, queue size
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        timer_period = 0.5 # seconds (how often to publish)
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # State variables for drawing the square
        self.state = 'forward' # 'forward' or 'turn'
        self.counter = 0
        self.side_length_steps = 4 # Number of steps to move forward (2 units at 0.5 speed)
        self.turn_steps = 2 # Number of steps to turn (pi/2 rad at pi/4 rad/s)

        self.get_logger().info('Square Publisher Node has been started. Turtle should draw a square.')

    def timer_callback(self):
        msg = Twist()
        if self.state == 'forward':
            if self.counter < self.side_length_steps:
                msg.linear.x = 0.5 # Move forward
                self.counter += 1
                self.get_logger().info(f'Moving forward {self.counter}/{self.side_length_steps}')
            else:
                msg.linear.x = 0.0 # Stop moving forward
                self.state = 'turn' # Switch to turning state
                self.counter = 0 # Reset counter for turning
                self.get_logger().info('Finished side, starting turn.')
        elif self.state == 'turn':
            if self.counter < self.turn_steps:
                msg.angular.z = math.pi / 4.0 # Turn counter-clockwise (0.785 rad/s)
                self.counter += 1
                self.get_logger().info(f'Turning {self.counter}/{self.turn_steps}')
            else:
                msg.angular.z = 0.0 # Stop turning
                self.state = 'forward' # Switch back to forward state
                self.counter = 0 # Reset counter for forward movement
                self.get_logger().info('Finished turn, starting side.')

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args) # Initialize ROS 2

    square_publisher = SquarePublisherNode() # Create node instance

    rclpy.spin(square_publisher) # Keep node alive

    # Cleanup
    square_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()