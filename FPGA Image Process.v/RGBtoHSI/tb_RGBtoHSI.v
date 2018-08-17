`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2018/08/16 14:32:08
// Design Name: 
// Module Name: tb_RGBtoHSI
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module tb_RGBtoHSI(

  );
  reg clk = 0;
  reg [7:0] R;
  reg [7:0] G;
  reg [7:0] B;
  reg RGBinEn;
  
  
  
  
 RGBtoHSI_WinPaint dut_RGBtoHSI_WinPaint(
  .clk(clk),
  .Rin(R),
  .Gin(G),
  .Bin(B),
  .RGBinEn(RGBinEn),
  .H(),
  .S(),
  .I(),
  .HSIoutEn()
  
  );
  
  always #5 clk = ~clk;
  
  initial
  begin
  	clk = 0;
  	R = 0;G = 0; B = 0;    
  	RGBinEn = 0;
  	#100;	
 	
 	  @(posedge clk);	#1;    
  	R = 255;G = 255; B = 0;RGBinEn =1;
 	
  	@(posedge clk);	#1;
  	R = 255;G = 0; B = 0;  	
  	
  	@(posedge clk);	#1;
  	R = 0;G = 255; B = 0;    
  	
  	@(posedge clk);	#1;  
  	R = 0;G = 255; B = 255;
  	                       
  	@(posedge clk);	#1;                         
  	R = 0;G = 0; B = 255;              
  	                       
  	@(posedge clk);	#1;   
  	R = 255;G = 0; B = 255; 
  	
  	@(posedge clk);	#1;
  	R = 192;G = 108; B = 63;
  	
  	@(posedge clk);	#1;
  	R = 79;G = 80; B = 37;
  	
  	@(posedge clk);	#1;
  	R = 88;G = 136; B = 83;     	 
  	
  	@(posedge clk);	#1;    
  	R = 90;G = 173; B = 194;
  	
  	@(posedge clk);	#1;    
  	R = 119;G = 119; B = 119;
  	
  	@(posedge clk);	#1; 
  	R = 252;G = 182; B = 243; 
  	
  	@(posedge clk);	#1; 
  	R = 0;G = 0; B = 0; 
  	
  	@(posedge clk);	#1; 
  	R = 255;G = 230; B = 231; 
  	
  	@(posedge clk);	#1;                  
  	R = 255;G = 255; B = 255;
  	
  	@(posedge clk);	#1;                  
  	R = 111;G = 222; B = 77;
  	 
  	@(posedge clk);	#1;
  	RGBinEn = 0;
  	
  	repeat(3)@(posedge clk)
  	
  	
  	#100;
  	$finish;
  end
  
    
    
endmodule
