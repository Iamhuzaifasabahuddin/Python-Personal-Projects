import click

operations = ['+', '-', '/', '^', '*', 'x', '**']


def validate(ctx, param, value):
    if value not in operations:
        raise click.BadParameter(f"Operand {value} is invalid\nChoose from {','.join(operations)}")
    return value


@click.command(name='calculator', help="First Input\tOperator\tSecond Input")
@click.argument('operand1', type=float)
@click.argument('operator', type=click.Choice(operations), callback=validate)
@click.argument('operand2', type=float)
@click.option('-v', '--verbose', is_flag=True, help='Provides with a verbose result')
def calculate(operand1, operator, operand2, verbose):
    try:
        if operator == '+':
            result = operand1 + operand2
        elif operator == '-':
            result = operand1 - operand2
        elif operator == '/':
            if operand2 == 0:
                raise click.ClickException("Zero Division is deemed invalid!")
            result = operand1 / operand2
        elif operator == '*' or operator == 'x':
            result = operand1 * operand2
        elif operator == '**' or operator == '^':
            result = operand1 ** operand2
        else:
            raise click.ClickException("Invalid operator")

        if verbose:
            click.echo(f"Calculating {operand1} {operator} {operand2}...")
            click.echo(f"Result for {operand1} {operator} {operand2} is {result =}")
        else:
            click.echo(result)
    except (ZeroDivisionError, ValueError, TypeError, click.ClickException) as error:
        click.echo(f"An error occurred: {error}")


if __name__ == '__main__':
    calculate()
