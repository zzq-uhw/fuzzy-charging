(helics_broker -t="zmq" --federates=3 --name=mainbroker &> ./broker.log &)
(exec python control_0.py &> ./control_0.log &)
(exec python new_para.py &> ./new_para.log &)
(gridlabd glm_0.glm &> ./glm_0.log &)
