/*
 * Logger.h
 *
 *  Created on: Jul 24, 2013
 *      Author: cforster
 */

#include <vikit/performance_monitor.h>
#include <string>

#ifndef LOGGER_H_
#define LOGGER_H_

#ifdef TRACE
  extern vk::PerformanceMonitor* g_permon;
  #define LOG(name,value) g_permon->log(std::string((name)),(value))
  #define START_TIMER(name) g_permon->startTimer((name))
  #define STOP_TIMER(name) g_permon->stopTimer((name))
#else
  #define LOG(name,value)
  #define START_TIMER(name)
  #define STOP_TIMER(name)
#endif


#endif /* LOGGER_H_ */
