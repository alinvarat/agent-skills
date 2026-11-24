4. **Manual duplex (2-sided)**:
   - Print odd pages first:
     ```bash
     lp -d EPSON_L3256 -o page-set=odd "FILE.pdf"
     ```
   - Wait for odd pages to finish (`lpstat -o EPSON_L3256` is empty), then ask the user to flip and reload the paper stack. Remind the user if needed that L3256 can feed the top sheet blank on the back pass (placing 1 blank sacrifice sheet on top avoids shifting the stack).
   - After user confirms reload, print even pages in reverse order:
     ```bash
     lp -d EPSON_L3256 -o page-set=even -o outputorder=reverse "FILE.pdf"
     ```
