**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

*TODO:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation
Refer below image files in the folder answer-img
01_pods_monitoring.jpg, 02_svc_monitoring.jpg, 03_pods_obs.jpg, 04_svc_obs.jpg, 05_pods_default.jpg, 06_svc_default.jpg
[Image](https://github.com/sumanbgl/CNAND_nd064_C4_Observability_Starter_Files/blob/master/Project_Starter_Files-Building_a_Metrics_Dashboard/answer-img/01_pods_monitoring.JPG)

## Setup the Jaeger and Prometheus source
*TODO:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.
Refer below image files in the folder answer-img
11_grafana_home_page.jpg, 12_grafana_ds.jpg

## Create a Basic Dashboard
*TODO:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.
Refer below image files in the folder answer-img
13_basic_dashboard.jpg

## Describe SLO/SLI
*TODO:* Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.
SLIs are the yardstick to quantify whether the goal mandated by the SLO is achieved. 
The SLIs for monthly uptime is measured by the number of times there was service unavailable error, number of unplanned downtimes, 
planned downed time for maintenance activity. 
The SLIs for request response time is measured by the total round trip time, latency experienced by the client.

## Creating SLI metrics.
*TODO:* It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs. 
Following are the 5 metrics to measure the specified SLIs.
 - Total round trip time. It includes the time spent on network and time the server takes to send back the response.
 - Total number of time service unavailable or internal server error seen in a specific period of time.
 - Average utilization of memory and CPU resources in a specific period of time.
 - Number of successfully processed requests in a specific time period.
 - Number for planned down-time of service in a specific time period.
 

## Create a Dashboard to measure our SLIs
*TODO:* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.
Refer below image files in the folder answer-img
14_backend_frontend_uptime_40x_errors.jpg, 15_backend_frontend_50x_errors.jpg

## Tracing our Flask App
*TODO:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here. Also provide a (screenshot) sample Python file containing a trace and span code used to perform Jaeger traces on the backend service.
Refer below image files in the folder answer-img
16_jaegar_01.jpg, 16_jaegar_02.jpg, 16_jaegar_03.jpg

## Jaeger in Dashboards
*TODO:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.
Refer below image files in the folder answer-img
17_graphana_dashboard_jaegar_01.jpg, 17_graphana_dashboard_jaegar_02.jpg, 17_graphana_dashboard_jaegar_03.jpg

## Report Error
*TODO:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue also include a screenshot of the tracer span to demonstrate how we can user a tracer to locate errors easily.

TROUBLE TICKET

Name: Http Status Code 500 on backend endpoint /star

Date: January 3, 2023, 15:42:53 GMT+5.30

Subject: Http Internal Server Error 500 on backend endpoint /star

Affected Area: File /app/app.py line 90 in add_star, name = request.json['name']

Severity: Critical

Description: backend endpoint /star is always failing with http status 500, blocking the addition of rating.
Please error is seen in the trace to be further investigated.

error kind: TypeError
error message: 'NoneType' object is not subscriptable
error stack: File /app/app.py line 90 in add_star, name = request.json['name']
Refer below image files in the folder answer-img
18_jaegar_error_trace_01.jpg, 18_jaegar_error_trace_02.jpg, 18_jaegar_error_trace_03.jpg

## Creating SLIs and SLOs
*TODO:* We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name four SLIs that you would use to measure the success of this SLO.
- Latency
- Errors
- Traffic
- Saturation

## Building KPIs for our plan
*TODO*: Now that we have our SLIs and SLOs, create a list of 2-3 KPIs to accurately measure these metrics as well as a description of why those KPIs were chosen. We will make a dashboard for this, but first write them down here.
Errors
 - Number of 500 errors : This is critical error happens due to bug in the software.Hence, it is important to measure.
 - Number of 40x errors: These are client side errors. It is important to analyze them to educate the clients about the software usage.

Saturation
 - Actual % CPU usage to understand the compute resource requirement and tune the software accordingly.
 - Actual % Memory usage to understand the compute resource requirement and tune the software accordingly.

Traffic
 - Number of http requests during non-peak period. To understand to define the autoscaling policies based on the time.
 - Number of http requests during the peak period. To understand to define the autoscaling policies based on the time.

Latency is measured using below KPI's
 - request time (milliseconds) for successful requests
 - request time (milliseconds) for failed requests

## Final Dashboard
*TODO*: Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  
Refer below image files in the folder answer-img
19_fd_av_resp_200_requests_01.jpg, 19_fd_av_resp_40x_50x_requests_02.jpg, 19_fd_failed_request_count_03.jpg, 
19_fd_total_requests_04.jpg, 19_fd_cpu_util_05.jpg, 19_fd_mem_util_06.jpg

19_fd_av_resp_200_requests_01.jpg -> Shows average response time for successful requests for frontend and backend service
19_fd_av_resp_40x_50x_requests_02.jpg -> Shows average response time for requests with status code 40x and 500 for frontend and backend service
19_fd_failed_request_count_03.jpg -> Show total number of requests with status code 40x and 500 for frontend and backend service
19_fd_total_requests_04.jpg -> Shows total number of requests for frontend and backend service
19_fd_cpu_util_05.jpg -> Shows CPU utilization for the container frontend and backend
19_fd_mem_util_06.jpg -> Shows Memory utilization for the container frontend and backend

