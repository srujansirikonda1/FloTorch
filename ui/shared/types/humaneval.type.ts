import { z } from "zod";

export const HumanEvalSchema = z.object({
    message: z.string().min(10, 'Message must be more than 10 characters'),
});

export type HumanEval = z.infer<typeof HumanEvalSchema>;