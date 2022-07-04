TFTP - Example

1. Download the .csv - Sample from this Page

https://www.kaggle.com/datasets/pedrohauy/sampledtftpattackcicddos2019

2. Execute csv2json.py. This converts the .csv in .json

3. Execute tftp-upload.sh. This splits the .json to smaller one and uploads the smaller one.

4. Open the Dashboard and go to Stack Management -> Saved Objects

5. Import the exportTFTP.ndjson

6. Check on the Saved Objects, if the tftp_mini was created and succesfully indexed. If yes go to Step 10.

7. Go to index pattern. -> Create Index Pattern

8. write tftp_mini* and go to next step.

9. Put Timestamp on the Timefield and finish everything.

10. Go to Dashboard (TFTP)

11. Top Right there is a calendar. Switch to 1st December 2018 14:00:00 - 1st December 2018 15:30:00

12. IP Selection - Choose which Packets should be shown.

13. TFTP Line IP - Differentiate the Packets between the Destination IP

14. timeline Expression - Overall Package

15. Heat Map TFTP - Same as TFTP Line IP, but in a different way

16. Avg Packet Size - Avg Packet Size from the Packages

19. Dest IP And Port - Destination for IP and Port in Heat Map.

20. You can see, The DDOS-Attack you can see it clearly.