#libraries
import click 
import time 
import os 


#global scope variables 

start_time = time.time() 
is_connected = False
config_path = os.path.join(os.getcwd(), 'Mirage/configs')

print(config_path)

@click.group()
def mirage_entry(): 

    click.echo("Success! Mirage is now connected! ")
   #  if is_connected: 
        
    #else: 
       # click.echo("There may be an error, try reconnecting again.")

@click.command()
@click.argument('sequence')

def config(sequence): 
    sequence_path = os.path.join(config_path, sequence)
    if os.path.exists(sequence_path): 
        click.echo(f"Initiating {sequence}")
    else: 
        click.echo(f"{sequence} does not exist")

mirage.add_command(config)


if __name__ == '__main__':
    mirage()