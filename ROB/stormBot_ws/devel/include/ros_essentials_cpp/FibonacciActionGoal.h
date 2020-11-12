// Generated by gencpp from file ros_essentials_cpp/FibonacciActionGoal.msg
// DO NOT EDIT!


#ifndef ROS_ESSENTIALS_CPP_MESSAGE_FIBONACCIACTIONGOAL_H
#define ROS_ESSENTIALS_CPP_MESSAGE_FIBONACCIACTIONGOAL_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>
#include <actionlib_msgs/GoalID.h>
#include <ros_essentials_cpp/FibonacciGoal.h>

namespace ros_essentials_cpp
{
template <class ContainerAllocator>
struct FibonacciActionGoal_
{
  typedef FibonacciActionGoal_<ContainerAllocator> Type;

  FibonacciActionGoal_()
    : header()
    , goal_id()
    , goal()  {
    }
  FibonacciActionGoal_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , goal_id(_alloc)
    , goal(_alloc)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef  ::actionlib_msgs::GoalID_<ContainerAllocator>  _goal_id_type;
  _goal_id_type goal_id;

   typedef  ::ros_essentials_cpp::FibonacciGoal_<ContainerAllocator>  _goal_type;
  _goal_type goal;





  typedef boost::shared_ptr< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> const> ConstPtr;

}; // struct FibonacciActionGoal_

typedef ::ros_essentials_cpp::FibonacciActionGoal_<std::allocator<void> > FibonacciActionGoal;

typedef boost::shared_ptr< ::ros_essentials_cpp::FibonacciActionGoal > FibonacciActionGoalPtr;
typedef boost::shared_ptr< ::ros_essentials_cpp::FibonacciActionGoal const> FibonacciActionGoalConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator1> & lhs, const ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator2> & rhs)
{
  return lhs.header == rhs.header &&
    lhs.goal_id == rhs.goal_id &&
    lhs.goal == rhs.goal;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator1> & lhs, const ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace ros_essentials_cpp

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "006871c7fa1d0e3d5fe2226bf17b2a94";
  }

  static const char* value(const ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x006871c7fa1d0e3dULL;
  static const uint64_t static_value2 = 0x5fe2226bf17b2a94ULL;
};

template<class ContainerAllocator>
struct DataType< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ros_essentials_cpp/FibonacciActionGoal";
  }

  static const char* value(const ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"\n"
"Header header\n"
"actionlib_msgs/GoalID goal_id\n"
"FibonacciGoal goal\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/Header\n"
"# Standard metadata for higher-level stamped data types.\n"
"# This is generally used to communicate timestamped data \n"
"# in a particular coordinate frame.\n"
"# \n"
"# sequence ID: consecutively increasing ID \n"
"uint32 seq\n"
"#Two-integer timestamp that is expressed as:\n"
"# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n"
"# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n"
"# time-handling sugar is provided by the client library\n"
"time stamp\n"
"#Frame this data is associated with\n"
"string frame_id\n"
"\n"
"================================================================================\n"
"MSG: actionlib_msgs/GoalID\n"
"# The stamp should store the time at which this goal was requested.\n"
"# It is used by an action server when it tries to preempt all\n"
"# goals that were requested before a certain time\n"
"time stamp\n"
"\n"
"# The id provides a way to associate feedback and\n"
"# result message with specific goal requests. The id\n"
"# specified must be unique.\n"
"string id\n"
"\n"
"\n"
"================================================================================\n"
"MSG: ros_essentials_cpp/FibonacciGoal\n"
"# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"#goal definition\n"
"int32 order\n"
;
  }

  static const char* value(const ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.goal_id);
      stream.next(m.goal);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct FibonacciActionGoal_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ros_essentials_cpp::FibonacciActionGoal_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "goal_id: ";
    s << std::endl;
    Printer< ::actionlib_msgs::GoalID_<ContainerAllocator> >::stream(s, indent + "  ", v.goal_id);
    s << indent << "goal: ";
    s << std::endl;
    Printer< ::ros_essentials_cpp::FibonacciGoal_<ContainerAllocator> >::stream(s, indent + "  ", v.goal);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ROS_ESSENTIALS_CPP_MESSAGE_FIBONACCIACTIONGOAL_H
