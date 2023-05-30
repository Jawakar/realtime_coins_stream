# Streaming Crypto Tokens in Real-Time

Real-time streaming of crypto tokens achieved using Kafka and Spark Structured Streaming, with seamless data warehousing integration.

![1685462457855](image/README/1685462457855.png)

## Table of Contents

* [Project Description](https://chat.openai.com/?model=text-davinci-002-render-sha#project-description)
* [Installation](https://chat.openai.com/?model=text-davinci-002-render-sha#installation)
* [Usage](https://chat.openai.com/?model=text-davinci-002-render-sha#usage)
* [Features](https://chat.openai.com/?model=text-davinci-002-render-sha#features)
* [Contributing](https://chat.openai.com/?model=text-davinci-002-render-sha#contributing)
* [License](https://chat.openai.com/?model=text-davinci-002-render-sha#license)

## Project Description

This project showcases the utilization of Kafka and Spark Structured Streaming to enable seamless real-time streaming of crypto tokens. By leveraging the power of these technologies, the project provides a robust and efficient solution for processing and analyzing streaming data. Additionally, the project incorporates a data warehousing solution to store the streaming data, facilitating further exploration and business intelligence purposes.

## Installation and Usage

To install and set up the project, please follow these steps:

1. Download the `requirements.txt` file, which contains the necessary Python dependencies. You can find it in the project repository.
2. Obtain GCP's free credits and start a VM instance. This instance will be used for running the project.
3. Use the provided `docker-compose.yml` file and replace "your_ip_address_here" with the actual IP address of your VM instance. This file will configure the necessary Docker containers for Kafka and other components.
4. Execute the following Docker commands to create a topic:
   <pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">docker exec -it kafka /bin/sh
   cd opt
   cd kafka_2.13-2.8.1
   ./bin/kafka-topics.sh --create --topic test_topic --bootstrap-server your_ip_address_here:9092 --replication-factor 1 --partitions 1
   </code></div></div></pre>
5. To verify the topic creation, execute the following command:
   <pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">./bin/kafka-topics.sh --list --bootstrap-server your_ip_address_here:9092
   </code></div></div></pre>
6. Create a producer to send messages to the topic:
   <pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">./bin/kafka-console-producer.sh --topic test_topic --bootstrap-server your_ip_address_here:9092
   </code></div></div></pre>
7. Use the provided `producer.py` script to produce messages to the Kafka topic.
8. Download the required JAR files that enable writing to BigQuery and configure them accordingly.
9. Finally, use the `consume_and_stream.py` script to consume messages from Kafka and stream them to the desired destination.
10. Execute the following `spark-submit` command:
    <pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 consume_and_stream.py
    </code></div></div></pre>

Make sure to replace "your_ip_address_here" with the actual IP address of your VM instance throughout the steps.

Please note that these instructions assume a working knowledge of Docker and GCP's VM instances.

## Acknowledgements

This project was inspired by the following resources:

* [DataTalksClub/data-engineering-zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_6_stream_processing), [YouTube](https://www.youtube.com/watch?v=KerNf0NANMo&ab_channel=DarshilParmar): Provides valuable insights on Kafka, compute engine, and BigQuery.
* [YouTube: Kafka installation using Docker and Docker Compose](https://www.youtube.com/watch?v=WnlX7w4lHvM&t=7s&ab_channel=CodeWithRajRanjan): Offers step-by-step guidance on setting up Kafka using Docker.
* [Fixing Hadoop connectors](https://github.com/GoogleCloudDataproc/hadoop-connectors/issues/618): Provides troubleshooting assistance for Hadoop connectors.

## License

This project is licensed under the [MIT License](https://github.com/Jawakar/realtime_coins_stream/blob/main/requirements.txt).
