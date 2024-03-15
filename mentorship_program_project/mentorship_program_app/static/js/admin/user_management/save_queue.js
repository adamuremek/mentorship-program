export class queue
{
    constructor()
    {
        this.actions = {}
        this.front_index = 0;
        this.back_index = 0;
    }

    enqueue(action) 
    {
        this.actions[this.back_index] = action
        this.back_index++
    }

    dequeue()
    {
        const action = this.actions[this.front_index]
        delete this.actions[this.front_index]
        this.front_index++
        return action
    }

    isEmpty()
    {
        return (this.front_index == 0 && this.back_index == 0)
    }
}