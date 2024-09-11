import apache_beam as beam

def print_hello(element):
    print(element)

# Define the Beam pipeline
def run():
    with beam.Pipeline() as pipeline:
        (
            pipeline
            | 'Create' >> beam.Create(['Hello, My World!'])
            | 'Print' >> beam.Map(print_hello)
        )

if __name__ == "__main__":
    run()
