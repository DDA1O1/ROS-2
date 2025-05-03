import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose # Import the Pose message type

class PoseSubscriberNode(Node):
    def __init__(self):
        super().__init__('pose_subscriber') # Node name
        # Create a subscriber:
        # takes message type, topic name, callback function, queue size
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose', # Topic to subscribe to
            self.listener_callback,
            10) # QoS profile depth
        self.subscription # prevent unused variable warning

        self.get_logger().info('Pose Subscriber Node has been started.')

    def listener_callback(self, msg):
        # This function is called whenever a message is received
        self.get_logger().info(f'Received pose: x={msg.x:.2f}, y={msg.y:.2f}, theta={msg.theta:.2f}')

def main(args=None):
    rclpy.init(args=args) # Initialize ROS 2 Python client library

    pose_subscriber = PoseSubscriberNode() # Create an instance of the node

    rclpy.spin(pose_subscriber) # Keep the node alive and processing callbacks

    # Cleanup when spin() exits (e.g., on Ctrl+C)
    pose_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()